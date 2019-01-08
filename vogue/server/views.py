from flask import make_response, flash, abort, url_for, redirect, render_template, request, session
from flask_login import login_user,logout_user, current_user, login_required
#from flask.ext.mail import Message
from flask_oauthlib.client import OAuthException

from vogue.server.extentions import adapter
from vogue.server.app import app
from vogue.server.utils import (find_recived_per_month, turn_around_times, 
                                find_concentration_defrosts, find_concentration_time,
                                find_concentration_amount)

from  datetime import date

THIS_YEAR = date.today().year
YEARS = [str(y) for y in range(2017, THIS_YEAR + 1)]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.form.get('page') == 'common':
        year = request.form.get('year')
        return redirect(url_for('common', year_of_interest=year))
    if request.form.get('page') == 'microbial':
        year = request.form.get('year')
        return redirect(url_for('microbial', year_of_interest=year))
    return render_template(
        'index.html',
        this_year = THIS_YEAR)

@app.route('/prepps/common/<year_of_interest>')
def common(year_of_interest):
    group_by = ['research','standard','priority']#,'express']
    group_key = "priority"
    received = find_recived_per_month(year_of_interest, group_by, group_key, adapter)
    received_application = find_recived_per_month(year_of_interest, group_by, group_key, adapter) #wrong groups!!!
    received_to_delivered = turn_around_times(year_of_interest, group_by, group_key, 
                                        'received_to_delivered' ,adapter) #wrong groups!!!
    received_to_prepped = turn_around_times(year_of_interest, group_by, group_key, 
                                        'received_to_prepped' ,adapter) #wrong groups!!!
    prepped_to_sequenced = turn_around_times(year_of_interest, group_by, group_key, 
                                        'prepped_to_sequenced' ,adapter) #wrong groups!!!
    sequenced_to_delivered = turn_around_times(year_of_interest, group_by, group_key, 
                                        'sequenced_to_delivered' ,adapter) #wrong groups!!!


    return render_template('common.html',
        header = 'Common',
        page_id = 'common',
        received = received,
        received_application = received_application,
        turnaround_times = received_to_delivered,
        received_to_delivered = received_to_delivered,
        received_to_prepped = received_to_prepped,
        prepped_to_sequenced = prepped_to_sequenced,
        sequenced_to_delivered = sequenced_to_delivered,
        year_of_interest=year_of_interest,
        this_year = THIS_YEAR,
        years = YEARS)

@app.route('/prepps/microbial/<year_of_interest>')
def microbial(year_of_interest):
    concentration_defrosts = find_concentration_defrosts(year_of_interest, adapter)
    concentration_time = find_concentration_time(year_of_interest, adapter)
    concentration_amount = find_concentration_amount(year_of_interest, adapter)
    return render_template('microbial.html',
        header = 'Microbial Samples',
        page_id = 'microbial',
        defrosts = concentration_defrosts,
        concentration_time = concentration_time,
        amount = concentration_amount,
        year_of_interest=year_of_interest,
        this_year = THIS_YEAR,
        years = YEARS)


@app.route('/sequencing/novaseq/<year_of_interest>')
def novaseq(year_of_interest):
    return render_template('novaseq.html',
        header = 'Nova Seq',
        page_id = 'novaseq',
        year_of_interest=year_of_interest,
        this_year = THIS_YEAR,
        years = YEARS)

@app.route('/sequencing/hiseqx/<year_of_interest>')
def hiseqx(year_of_interest):
    return render_template('hiseqx.html',
        header = 'HiseqX',
        page_id = 'hiseqx',
        year_of_interest=year_of_interest,
        this_year = THIS_YEAR,
        years = YEARS)

