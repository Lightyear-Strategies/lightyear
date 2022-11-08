from flask_login import login_required
from flask_app.scripts.create_flask_app import db
from flask import render_template, request, current_app
from datetime import datetime, timedelta
import pandas as pd
import os
from time import time

import traceback
import sys
import logging
from logging import StreamHandler, Formatter

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

handler = StreamHandler(stream=sys.stdout)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))
logger.addHandler(handler)


def removeDBdups():
    """
    removes duplicates from SQLite DB, does not need to be run often, as the addDBData function now checks for duplicates
    """
    whole_db = pd.read_sql_table('haros', db.engine)
    print(whole_db)
    whole_db.drop_duplicates(subset=['Summary'], inplace=True)
    print(whole_db)
    whole_db.to_sql('haros', con=db.engine, index=False, if_exists='replace')
    new_db = pd.read_sql_table('haros', db.engine)
    print(new_db)


def addDBData(df: pd.DataFrame):  # (file):
    """
    Adds data to SQLite DB and checks for duplicates
    @param:    csv file with parsed haros
    @return:   None
    """
    # checking for duplicates
    try:
        try:
            whole_db = pd.read_sql_table('haros', db.engine, index_col='index')
            logger.info(len(whole_db))
            logger.info(whole_db.columns)
            whole_db.sort_index(inplace=True, ascending= True)
            res = pd.concat([whole_db, df])
        except Exception:
            logger.info('\nSmall addDBData Problem:')
            res = df
            traceback.print_exc(file=sys.stdout)
        logger.info(len(res))
        res.drop_duplicates(subset=['Summary'], inplace=True)
        logger.info(len(res))
        res.reset_index(drop=True, inplace=True)
        res.sort_index(inplace=True, ascending=False)

        # Load data to database
        logger.info(res.columns)
        res.to_sql(name='haros', con=db.engine,
                   index=True, if_exists='replace')
    except Exception:
        logger.info('\nBig addDBData Problem:')
        traceback.print_exc(file=sys.stdout)


@login_required
def show_haro_table():
    """
    Shows Haro Table
    @param:    None
    @return:   Haros table
    """
    updated = str(get_last_updated())
    return render_template('HaroTable/haroTableView.html', title='LyS Haros Database', date_updated=updated.split()[0]+" "+updated.split()[1][:8])
    # return render_template('HaroTable/haroTableView.html', title='LyS Haros Database', date_updated=updated.split()[0], time_updated=updated.split()[1][:8])


def get_last_updated():
    """returns a datetime of the most recently updated haro"""
    Haros = db.Table('haros', db.metadata, autoload=True, autoload_with=db.engine)
    most_recent_date_received = db.session.query(Haros.columns.DateReceived).first()[0]
    return datetime.fromisoformat(most_recent_date_received)

# def adding_used_unused(option: str = None, id: str = None):
#     """
#     Changes value in "Used" column of certain haro by using id
#     Values can be "Used" or "None"
#     @param:    option and id in the table
#     @return:   string
#     """
#
#     Haros = db.Table('haros', db.metadata, autoload=True, autoload_with=db.engine)
#     query = db.session.query(Haros).filter(Haros.columns.index == int(id))
#     #print(query.all())
#
#     if option == "add":
#         query.update({Haros.columns.Used : "Used" })
#         db.session.commit()
#
#     elif option == "remove":
#         query.update({Haros.columns.Used: "None"})
#         db.session.commit()
#
#    # print(query.all())
#
#     return "OK"


def serve_data(option=None):
    """
    Sorts the table, returns searched data
    @param:    None/option
    @return:   table entries
    """
    start_t = time()

    Haros = db.Table('haros', db.metadata, autoload=True,
                     autoload_with=db.engine)
    # print(Haros.columns.DateReceived.all_())
    query = db.session.query(Haros)  # .all()

    # fresh queries
    if option == "fresh":
        most_recent_update = get_last_updated()
        freshmark = most_recent_update.date() - timedelta(days=1)
        query = query.filter(Haros.columns.DateReceived >= freshmark)

    # search filter
    print('Arguments:', end=' ')
    print(request.args)

    keywords = request.args.get('keywords')
    mediaOutlet = request.args.get('mediaOutlet')
    category = request.args.get('category')
    dateBefore = request.args.get('dateBefore')
    dateAfter = request.args.get('dateAfter')

    if dateBefore:
        query = query.filter(db.or_(
            Haros.columns.DateReceived <= datetime.strptime(
                dateBefore, '%m/%d/%Y %H:%M:%S')
        ))

    if dateAfter:
        query = query.filter(db.or_(
            Haros.columns.DateReceived >= datetime.strptime(
                dateAfter, '%m/%d/%Y %H:%M:%S')
        ))

    if keywords:
        query = query.filter(db.or_(
            Haros.columns.Query.like(f'%{keywords}%'),
            Haros.columns.Summary.like(f'%{keywords}%'),
            Haros.columns.Requirements.like(f'%{keywords}%')
        ))

    if mediaOutlet:
        query = query.filter(db.or_(
            Haros.columns.MediaOutlet.like(f'%{mediaOutlet}%')
        ))

    if category:
        query = query.filter(
            Haros.columns.Category.like(f'%{category}%')
        )

    total_filtered = query.count()
    # sorting
    # order = []
    # i = 0
    # while True:
    #
    #     col_index = request.args.get(f'order[{i}][column]')
    #     if col_index is None:
    #         break
    #     col_name = request.args.get(f'columns[{col_index}][data]')
    #     if col_name not in ['Category','MediaOutlet','DateReceived']:
    #         col_name = 'TimeStamp'
    #     if col_name == 'DateReceived':
    #         col_name = 'TimeStamp'
    #
    #     # gets descending sorting
    #     descending = request.args.get(f'order[{i}][dir]') == 'desc'
    #
    #     desired_col = getattr(Haros.columns,col_name)
    #
    #     #decending
    #     if descending:
    #         desired_col = desired_col.desc()
    #     order.append(desired_col)
    #
    #     i += 1
    #
    # # ordering
    # if order:
    #     query = query.order_by(*order)

    # pagination
    start = request.args.get('start', type=int)
    length = request.args.get('length', type=int)
    query = query.offset(start).limit(length)

    end_t = time()
    print(end_t - start_t)

    # response to be shown on HTML side
    return {
        'data': [dict(haro) for haro in query],
        'recordsFiltered': total_filtered,
        'recordsTotal': query.count(),
        'draw': request.args.get('draw', type=int),
    }
