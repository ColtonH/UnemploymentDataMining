from django.db import connection
from data.models import UnemploymentByStateMonthly, UsState, NatalityByStateYearly, MortalityByStateYearly
from django.db.models import Avg, Max, Min, Sum, F

# Returns a list of ovailable years for a variable (using min and max)
def getAvailableYearChoices(model,variable):
    null_filter = {variable+'__isnull':False}
    queryset = model.objects
    max_year = queryset.filter(**null_filter).aggregate(Max('year'))['year__max']
    min_year = queryset.filter(**null_filter).aggregate(Min('year'))['year__min']
    choices = tuple([(i,i) for i in range(min_year,max_year+1)])
    return choices,min_year,max_year

# Returns data to do clustering or other technique between unemployment and other 
# variable aggregated by year and state, being able to fileter bi year /state.
# The aggregation for unemployment is done using Avg and for the other variable
# using Sum
def get_unemp_vs_var_from_database_paired(model,variable,min_year,max_year,states=None,years=None,normalize_data=True,difference_unemp=False,difference_var=True):
    # Get table names for sql statements
    unemployment_table_name = UnemploymentByStateMonthly._meta.db_table
    model_table_name = model._meta.db_table

    # Prepare SQL filters (years, state)
    filter_states = ''
    if states:
        filter_states+=' and state_id in ('
        for state in states: # Construct in statement
            filter_states += str(state.id)+','
        filter_states= filter_states[:-1] +')' # Remove last comma

    filter_years = 'year>='+str(min_year)+' and year<='+str(max_year)+' '
    if years: # Filter years if user selects a range
        filter_years=' year in (' 
        for year in years: # Construct in statement
            filter_years += str(year)+','
        filter_years= filter_years[:-1] +')' # Remove last comma
    # Build base SQL statements to avoid code repetition and to make it clearer.
    # Filters are only set on unemployment qury, as the outher where inner join on state
    # and year will filter the results not contained in those states and / or years
    if not difference_unemp:
        sql_unemployment='''SELECT state_id, year, Avg(value) as avg_value 
                    from %s
                    where %s %s
                    GROUP BY year, state_id
                    ORDER BY state_id,year
                    ''' % (unemployment_table_name,filter_years,filter_states)
    else:
        sql_unemployment='''SELECT VAR.state_id,VAR.year,(VAR.variable-VAR_SR.variable) as avg_value
                    FROM
                        (SELECT state_id, year, Avg(value) as variable 
                        from %s
                        where %s %s
                        group by state_id,year) as VAR,
                        (SELECT state_id, year+1 as year, Avg(value) as variable 
                        from %s
                        where %s %s
                        group by state_id,year) as VAR_SR
                    WHERE VAR.state_id = VAR_SR.state_id and VAR.year = VAR_SR.year
        ''' %  (unemployment_table_name,filter_years,filter_states,unemployment_table_name,filter_years,filter_states)

    if not difference_var:    
        sql_variable ='''SELECT state_id, year, Sum(%s) as variable 
                    from %s
                    where %s %s
                    group by state_id,year
                ''' % (variable,model_table_name,filter_years,filter_states,)
    else:
        sql_variable ='''SELECT VAR.state_id,VAR.year,(VAR.variable-VAR_SR.variable) as variable
                        FROM
                            (SELECT state_id, year, Sum(%s) as variable 
                                                from %s
                                                where %s %s
                                                group by state_id,year) as VAR,
                            (SELECT state_id, year+1 as year, Sum(%s) as variable 
                                                from %s
                                                where %s %s
                                                group by state_id,year) as VAR_SR
                        WHERE VAR.state_id = VAR_SR.state_id and VAR.year = VAR_SR.year
                    ''' % (variable,model_table_name,filter_years,filter_states,variable,model_table_name,filter_years,filter_states,)
    # If user selects to normalize data, we need a pretty complex sql to do
    # normalization from the database.
    if normalize_data==True:
        sql =  '''  SELECT STATE.name as state_name, STATE.code as state_code, Q1.year, Q1.unemployment,Q2.variable
                    FROM
                    (SELECT AA.state_id, AA.year, (AA.avg_value-DD.min_value)::float/(DD.max_value-DD.min_value) as unemployment
                    FROM
                        (%s) as AA,
                        (SELECT CC.state_id,  Max(CC.avg_value) as max_value,Min(CC.avg_value) as min_value 
                        from 
                            (%s) as CC
                        GROUP BY CC.state_id
                        ) as DD
                    where AA.state_id = DD.state_id
                    ) as Q1,

                    (SELECT TT.state_id,TT.year, (TT.variable-YY.min_variable)::float/(YY.max_variable-YY.min_variable) as variable
                    FROM
                        (%s) as TT,
                        (SELECT GG.state_id , Max(GG.variable) as max_variable,Min(GG.variable) as min_variable
                            FROM (%s) AS GG
                        GROUP BY GG.state_id
                        ) as YY
                    where TT.state_id = YY.state_id
                    ) as Q2,
                    data_usstate as STATE
                    where Q1.state_id=Q2.state_id and Q1.year = Q2.year and Q1.state_id=STATE.id
                    order by STATE.name,Q1.year
                                ''' % (sql_unemployment,sql_unemployment,sql_variable,sql_variable)
    else:
        sql ='''SELECT STATE.name as state_name, STATE.code as state_code, Q1.year, Q1.avg_value as unemployment,Q2.variable
            FROM 
                (%s) as Q1,
                (%s) as Q2,
                data_usstate as STATE
            where Q1.state_id=Q2.state_id and Q1.year = Q2.year and Q1.state_id=STATE.id
            order by STATE.name,Q1.year
        ''' % (sql_unemployment,sql_variable)
    cursor = connection.cursor()
    cursor.execute(sql)
    data=cursor.fetchall()
    data = [{'state_name':row[0],'state_code':row[1],'year':row[2],'unemployment':row[3],'variable':row[4]} for row in data]
    return data

