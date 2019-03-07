from flask import url_for, redirect, render_template, request, Blueprint, current_app

from vogue.constants.constants import YEARS, THIS_YEAR
from vogue.server.utils import ( find_concentration_defrosts, find_concentration_amount, value_per_month, plot_atributes)

app = current_app
blueprint = Blueprint('server', __name__)

@blueprint.route('/', methods=['GET', 'POST'])
def index():
    year = request.form.get('year')
    if not year:
        year = THIS_YEAR

    if request.form.get('page') == 'turn_around_times':
        return redirect(url_for('server.turn_around_times', year=year))
    if request.form.get('page') == 'samples':
        return redirect(url_for('server.common_samples', year=year))
    if request.form.get('page') == 'microbial':
        return redirect(url_for('server.microbial', year=year))
    if request.form.get('page') == 'wgs':
        return redirect(url_for('server.wgs', year=year))
    if request.form.get('page') == 'lucigen':
        return redirect(url_for('server.lucigen', year=year))
    if request.form.get('page') == 'target_enrichment':
        return redirect(url_for('server.target_enrichment', year=year))

    return render_template(
        'index.html',
        year_of_interest = year)

@blueprint.route('/common/turn_around_times/<year>')
def turn_around_times(year):

    y_vals = ['received_to_delivered', 'received_to_prepped', 'prepped_to_sequenced', 'sequenced_to_delivered']

    results_grouped_by_prio = value_per_month(app.adapter, year, y_vals, "priority")
    results_grouped_by_cat = value_per_month(app.adapter, year, y_vals, "category")
    y_axis_label = 'Days'

    # plot titles
    r2d_c = 'Time from recieved to delivered (grouped by application tag category)'
    r2d_p = 'Time from recieved to delivered (grouped by priority)'
    r2p_c = 'Time from recieved to prepped (grouped by application tag category)'
    r2p_p = 'Time from recieved to prepped (grouped by priority)'
    p2s_c = 'Time from prepped to sequenced (grouped by application tag category)'
    p2s_p = 'Time from prepped to sequenced (grouped by priority)'                            
    s2d_c = 'Time from sequenced to delivered (grouped by application tag category)'
    s2d_p = 'Time from sequenced to delivered (grouped by priority)'

    return render_template('turn_around_times.html',
        header = 'Turn Around Times',
        page_id = 'turn_around_times',
        data_prio = results_grouped_by_prio,
        data_cat = results_grouped_by_cat,
        received_to_delivered_cat = plot_atributes( title = r2d_c , y_axis_label = y_axis_label),
        received_to_delivered_prio = plot_atributes( title = r2d_p , y_axis_label = y_axis_label),
        received_to_prepped_cat = plot_atributes( title = r2p_c , y_axis_label = y_axis_label),
        received_to_prepped_prio = plot_atributes( title = r2p_p , y_axis_label = y_axis_label),
        prepped_to_sequenced_cat = plot_atributes( title = p2s_c , y_axis_label = y_axis_label),
        prepped_to_sequenced_prio = plot_atributes( title = p2s_p , y_axis_label = y_axis_label),
        sequenced_to_delivered_cat = plot_atributes( title = s2d_c , y_axis_label = y_axis_label),
        sequenced_to_delivered_prio = plot_atributes( title = s2d_p , y_axis_label = y_axis_label),
        year_of_interest=year,
        years = YEARS)


@blueprint.route('/common/samples/<year>')
def common_samples(year):
    y_vals = ['count']
    data_cat = value_per_month(app.adapter, year, y_vals, 'category')
    data_prio = value_per_month(app.adapter, year, y_vals, 'priority')
    y_axis_label = 'Nr of samples'

    return render_template('samples.html',
        header = 'Samples',
        page_id = 'samples',
        data_prio = data_prio['count'],
        data_cat = data_cat['count'],
        plot_prio = plot_atributes( title = 'Received samples per month (grouped by priority)' , y_axis_label = y_axis_label),
        plot_cat = plot_atributes( title = 'Received samples per month (grouped by aplication tag)' , y_axis_label = y_axis_label),
        year_of_interest=year,
        years = YEARS)


@blueprint.route('/prepps/microbial/<year>')
def microbial(year):
    y_vals = ['microbial_library_concentration']
    data = value_per_month(app.adapter, year, y_vals, "strain")
    return render_template('microbial.html',
        header = 'Microbial Samples',
        page_id = 'microbial',
        data = data['microbial_library_concentration'], 
        plot_atributes = plot_atributes( title = 'Microbial' , y_axis_label = 'Concentration (nM)'),
        year_of_interest=year,
        years = YEARS)


@blueprint.route('/prepps/target_enrichment/<year>')
def target_enrichment(year):
    y_vals = ['library_size_post_hyb', 'library_size_pre_hyb']
    data = value_per_month(app.adapter, year, y_vals, "source")
    y_axis_label = 'library size'

    return render_template('target_enrichment.html',
        header = 'Target enrichment (exom/panels)',
        page_id = 'target_enrichment',
        data_pre_hyb = data['library_size_pre_hyb'],
        data_post_hyb = data['library_size_post_hyb'],
        plot_post_hyb = plot_atributes( title = 'Post-hybridization QC' , y_axis_label = y_axis_label),
        plot_pre_hyb = plot_atributes( title = 'Pre-hybridization QC' , y_axis_label = y_axis_label),
        year_of_interest=year,
        years = YEARS)


@blueprint.route('/prepps/wgs/<year>')
def wgs(year):
    concentration_time = value_per_month(app.adapter, year, ['nr_defrosts-concentration'])
    concentration_defrosts = find_concentration_defrosts(adapter = app.adapter, year = year)

    return render_template('wgs.html',
        header = 'WGS illumina PCR-free',
        page_id = 'wgs',
        concentration_defrosts = concentration_defrosts,
        concentration_time = concentration_time['nr_defrosts-concentration'],
        plot_atributes = plot_atributes( title = 'wgs illumina PCR-free' , y_axis_label = 'Concentration (nM)'),
        year_of_interest=year,
        years = YEARS)


@blueprint.route('/prepps/lucigen/<year>')
def lucigen(year):
    amount_concentration_time = value_per_month(app.adapter, year, ['amount-concentration'])
    concentration_amount = find_concentration_amount(adapter = app.adapter, year = year)

    return render_template('lucigen.html',
        header = 'Lucigen PCR-free',
        page_id = 'lucigen',
        amount_concentration_time = amount_concentration_time['amount-concentration'],
        plot_atributes = plot_atributes( title = 'lucigen PCR-free', y_axis_label = 'Concentration (nM)'),
        amount = concentration_amount,
        year_of_interest=year,
        years = YEARS)


@blueprint.route('/sequencing/novaseq/<year>')
def novaseq(year):

    return render_template('novaseq.html',
        header = 'Nova Seq',
        page_id = 'novaseq',
        year_of_interest=year,
        years = YEARS)


@blueprint.route('/sequencing/hiseqx/<year>')
def hiseqx(year):

    return render_template('hiseqx.html',
        header = 'HiseqX',
        page_id = 'hiseqx',
        year_of_interest=year,
        years = YEARS)
