import streamlit as st
import pandas as pd
import numpy as np
from st_aggrid import AgGrid
from st_aggrid.grid_options_builder import GridOptionsBuilder

from millify import millify

from pyecharts import options as opts
from pyecharts.charts import Bar, Line
from streamlit_echarts import st_pyecharts,st_echarts


st.set_page_config(page_title="Kiteko Dashboard", page_icon="📈", layout="wide")
st.markdown(""" <style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style> """, unsafe_allow_html=True)

#######    DATA PREPROCESSING   #########
monthly_data = pd.read_excel("FN-2016-2019(1).xlsx", sheet_name="Monthly", skiprows=2, header=0).fillna(0)
monthly_data = monthly_data[monthly_data['Account Item'] != 0][1:]
monthly_data = monthly_data.set_index("Account Item").astype(int)

ytd_data = pd.read_excel("FN-2016-2019(1).xlsx", sheet_name="YTD", skiprows=2, header=0).fillna(0)
ytd_data = ytd_data[ytd_data['Account Item'] != 0][1:]
ytd_data = ytd_data.set_index("Account Item").astype(int)

#raw_data = pd.read_excel("FN-2016-2019(1).xlsx", sheet_name="Monthly", skiprows=2, header=0).fillna(0)
quarterly_data = pd.read_excel("FN-2016-2019(1).xlsx", sheet_name="Quarterly", skiprows=3).fillna(0)
quarterly_data = quarterly_data[quarterly_data['Account Item'] != 0]
quarterly_data = quarterly_data.set_index("Account Item").astype(int)

annual_data = pd.read_excel("FN-2016-2019(1).xlsx", sheet_name="Annually", skiprows=3).fillna(0)
annual_data = annual_data[annual_data['Account Item'] != 0]
annual_data = annual_data.set_index("Account Item").astype(int)

def display_df(df, column):
    use_data = df[df.index.str.contains(column)].reset_index()
    gb = GridOptionsBuilder.from_dataframe(use_data)
    gb.configure_pagination()
    gridOptions = gb.build()
    return AgGrid(use_data, gridOptions=gridOptions)

def display_data(df, column):
    return df[df.index.str.contains(column)]

all_ = "Total"
cocoa_ = "Cocoa"
cashew_ = "Cashew"
other_ = "Other Business"
oil_ = "Oil Business"
black_ = "Black Oil"
ph_ = "Private Hauliers"


st.title('KITEKO Dashboard')
st.sidebar.subheader("December 2018")
currency = st.sidebar.radio("Currency", ("GHS", "USD"))
period = st.sidebar.radio("Period", ("FTM", "YTD", "Quarterly", "Annually"))
#timeframe = st.radio("Time Frame", ("Monthly", "Quarterly", "Annually"))
units = st.sidebar.radio("Select Business", (all_, cocoa_, cashew_, other_, oil_, black_, ph_))
comparison = st.sidebar.radio("Basis of Comparison", ("Previous Year", "Previous Period", "Budget", "Forecast"))


##############  FOR THE MONTH   ##############################
if period == "FTM":
    def business_wise():
        rev_metric = display_data(monthly_data, units).T.iloc[-1].loc[units + " Revenue"]
        rev_metric1 = display_data(monthly_data, units).T.iloc[-13].loc[units + " Revenue"]
        dc_metric = display_data(monthly_data, units).T.iloc[-1].loc[units + " GC"]
        dc_metric1 = display_data(monthly_data, units).T.iloc[-13].loc[units + " GC"]
        nc_metric = display_data(monthly_data, units).T.iloc[-1].loc[units + " NC"]
        nc_metric1 = display_data(monthly_data, units).T.iloc[-13].loc[units + " NC"]
        ebita_metric = display_data(monthly_data, units).T.iloc[-1].loc[units + " EBITA"]
        ebita_metric1 = display_data(monthly_data, units).T.iloc[-13].loc[units + " EBITA"]
        pbt_metric = display_data(monthly_data, units).T.iloc[-1].loc[units + " PBT"]
        pbt_metric1 = display_data(monthly_data, units).T.iloc[-13].loc[units + " PBT"]
        trip_metric = display_data(monthly_data, units).T.iloc[-1].loc[units + " Trips"]
        trip_metric1 = display_data(monthly_data, units).T.iloc[-13].loc[units + " Trips"]
        km_metric = display_data(monthly_data, units).T.iloc[-1].loc[units + " Distance"]
        km_metric1 = display_data(monthly_data, units).T.iloc[-13].loc[units + " Distance"]
        dc_margin = (dc_metric / rev_metric) * 100
        dc_margin1 = (dc_metric1 / rev_metric1) * 100
        nc_margin = (pbt_metric / rev_metric) * 100
        nc_margin1 = (pbt_metric1 / rev_metric1) * 100

        html_line="""<hr style="display: block; margin-top:0.2em; margin-bottom:0.2em; margin-left:auto; margin-right:auto; border-style:inset; border-width:2.5px;"></h1>"""
        st.markdown(html_line, unsafe_allow_html=True)
        kpi1, kpi2, kpi3, kpi4, kpi5, kpi6, kpi7, kpi8, kpi9 = st.columns(9)
        kpi1.metric(label = "Trips", value = int(trip_metric), delta = int(trip_metric - trip_metric1))
        kpi2.metric(label = "Revenue", value = millify(int(rev_metric), precision=2), delta = millify(int(rev_metric - rev_metric1), precision=0))
        kpi3.metric(label = "Gross Contribution", value = millify(int(dc_metric), precision=2), delta = millify(int(dc_metric - dc_metric1), precision=0))
        kpi4.metric(label = "Net Contribution", value = millify(int(nc_metric), precision=2), delta = millify(int(nc_metric - nc_metric1), precision=0))
        kpi5.metric(label = "EBITDA", value = millify(int(ebita_metric), precision=2), delta = millify(int(ebita_metric - ebita_metric1), precision=0))
        kpi6.metric(label = "PBT", value = millify(int(pbt_metric), precision=2), delta = millify(int(pbt_metric - pbt_metric1), precision=0))
        kpi7.metric(label = "Gross Profit Margin", value = "%.0f" %dc_margin, delta = "%.0f" %(dc_margin - dc_margin1))
        kpi8.metric(label = "Net Profit Margin", value = "%.0f" %nc_margin, delta = "%.0f" %(nc_margin - nc_margin1))
        kpi9.metric(label = "Distance Covered", value = millify(int(km_metric), precision=0), delta = millify(int(km_metric - km_metric1), precision=0))
        st.markdown(html_line, unsafe_allow_html=True)

        ### BAR PLOT ######
        account_type = st.selectbox("Account Item", display_data(monthly_data, units).T.columns.tolist())

        v1 = display_data(monthly_data, units).T[account_type].values.tolist()
        attr = [i for i in display_data(monthly_data, units)]#.T.loc["Revenue"].index.format()]

        b = (Bar()
            .add_xaxis(attr)
            .add_yaxis(account_type, v1)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="Monthly Trends", subtitle="2016-2018 Trends in GHS '000 except Trips")))
        st_pyecharts(b)

        value1 = display_data(monthly_data, units).T[account_type][:12].values.tolist()
        value2 = display_data(monthly_data, units).T[account_type][12:24].values.tolist()
        value3 = display_data(monthly_data, units).T[account_type][24:36].values.tolist()
        attribute1 = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        c = (Bar()
            .add_xaxis(attribute1)
            .add_yaxis("2016", value1)
            .add_yaxis("2017", value2)
            .add_yaxis("2018", value3)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="2016-2018 Monthly Comparison", subtitle=account_type+" Comparison for "+units)))
        st_pyecharts(c)

        data_show = st.checkbox('Show Data')
        if data_show:
            display_df(monthly_data, units)

        
#####################  YEAR TO DATE    ########################################
elif period == "YTD":
    def business_wise():
        rev_metric = display_data(ytd_data, units).T.iloc[-1].loc[units + " Revenue"]
        rev_metric1 = display_data(ytd_data, units).T.iloc[-13].loc[units + " Revenue"]
        dc_metric = display_data(ytd_data, units).T.iloc[-1].loc[units + " GC"]
        dc_metric1 = display_data(ytd_data, units).T.iloc[-13].loc[units + " GC"]
        nc_metric = display_data(ytd_data, units).T.iloc[-1].loc[units + " NC"]
        nc_metric1 = display_data(ytd_data, units).T.iloc[-13].loc[units + " NC"]
        ebita_metric = display_data(ytd_data, units).T.iloc[-1].loc[units + " EBITA"]
        ebita_metric1 = display_data(ytd_data, units).T.iloc[-13].loc[units + " EBITA"]
        pbt_metric = display_data(ytd_data, units).T.iloc[-1].loc[units + " PBT"]
        pbt_metric1 = display_data(ytd_data, units).T.iloc[-13].loc[units + " PBT"]
        trip_metric = display_data(ytd_data, units).T.iloc[-1].loc[units + " Trips"]
        trip_metric1 = display_data(ytd_data, units).T.iloc[-13].loc[units + " Trips"]
        km_metric = display_data(ytd_data, units).T.iloc[-1].loc[units + " Distance"]
        km_metric1 = display_data(ytd_data, units).T.iloc[-13].loc[units + " Distance"]
        dc_margin = dc_metric / rev_metric
        dc_margin1 = dc_metric1 / rev_metric1
        nc_margin = pbt_metric / rev_metric
        nc_margin1 = pbt_metric1 / rev_metric1

        html_line="""<hr style="display: block; margin-top:0.2em; margin-bottom:0.2em; margin-left:auto; margin-right:auto; border-style:inset; border-width:2.5px;"></h1>"""
        st.markdown(html_line, unsafe_allow_html=True)
        kpi1, kpi2, kpi3, kpi4, kpi5, kpi6, kpi7, kpi8 = st.columns(8)
        kpi1.metric(label = "Trips", value = int(trip_metric), delta = int(trip_metric - trip_metric1))
        kpi2.metric(label = "Revenue", value = millify(int(rev_metric), precision=2), delta = millify(int(rev_metric - rev_metric1), precision=2))
        kpi3.metric(label = "Gross Contribution", value = millify(int(dc_metric), precision=2), delta = millify(int(dc_metric - dc_metric1), precision=2))
        kpi4.metric(label = "Net Contribution", value = millify(int(nc_metric), precision=2), delta = millify(int(nc_metric - nc_metric1), precision=2))
        kpi5.metric(label = "EBITDA", value = millify(int(ebita_metric), precision=2), delta = millify(int(ebita_metric - ebita_metric1), precision=2))
        kpi6.metric(label = "PBT", value = millify(int(pbt_metric), precision=2), delta = millify(int(pbt_metric - pbt_metric1), precision=2))
        kpi7.metric(label = "Gross Profit Margin", value = "%.2f" %dc_margin, delta = "%.2f" %(dc_margin - dc_margin1))
        kpi8.metric(label = "Net Profit Margin", value = "%.2f" %nc_margin, delta = "%.2f" %(nc_margin - nc_margin1))
        st.markdown(html_line, unsafe_allow_html=True)

        ### BAR PLOT ######
        account_type = st.selectbox("Account Item", display_data(ytd_data, units).T.columns.tolist())
        v1 = display_data(ytd_data, units).T[account_type].values.tolist()
        attr = [i for i in display_data(ytd_data, units)]#.T.loc["Revenue"].index.format()]

        b = (Bar()
            .add_xaxis(attr)
            .add_yaxis(account_type, v1)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="Monthly Trends", subtitle="2016-2018 Trends in GHS '000 except Trips")))
        st_pyecharts(b)

        value1 = display_data(ytd_data, units).T[account_type][:12].values.tolist()
        value2 = display_data(ytd_data, units).T[account_type][12:24].values.tolist()
        value3 = display_data(ytd_data, units).T[account_type][24:36].values.tolist()
        attribute1 = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

        c = (Bar()
            .add_xaxis(attribute1)
            .add_yaxis("2016", value1)
            .add_yaxis("2017", value2)
            .add_yaxis("2018", value3)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="2016-2018 Monthly Comparison", subtitle=account_type+" Comparison for "+units)))
        st_pyecharts(c)

        data_show = st.checkbox('Show Data')
        if data_show:
            display_df(ytd_data, units)


elif period == "Quarterly":
    def business_wise():
        rev_metric = display_data(quarterly_data, units).T.iloc[-1].loc[units + " Revenue"]
        rev_metric1 = display_data(quarterly_data, units).T.iloc[-5].loc[units + " Revenue"]
        dc_metric = display_data(quarterly_data, units).T.iloc[-1].loc[units + " GC"]
        dc_metric1 = display_data(quarterly_data, units).T.iloc[-5].loc[units + " GC"]
        nc_metric = display_data(quarterly_data, units).T.iloc[-1].loc[units + " NC"]
        nc_metric1 = display_data(quarterly_data, units).T.iloc[-5].loc[units + " NC"]
        ebita_metric = display_data(quarterly_data, units).T.iloc[-1].loc[units + " EBITA"]
        ebita_metric1 = display_data(quarterly_data, units).T.iloc[-5].loc[units + " EBITA"]
        pbt_metric = display_data(quarterly_data, units).T.iloc[-1].loc[units + " PBT"]
        pbt_metric1 = display_data(quarterly_data, units).T.iloc[-5].loc[units + " PBT"]
        trip_metric = display_data(quarterly_data, units).T.iloc[-1].loc[units + " Trips"]
        trip_metric1 = display_data(quarterly_data, units).T.iloc[-5].loc[units + " Trips"]
        km_metric = display_data(quarterly_data, units).T.iloc[-1].loc[units + " Distance"]
        km_metric1 = display_data(quarterly_data, units).T.iloc[-5].loc[units + " Distance"]
        dc_margin = dc_metric / rev_metric
        dc_margin1 = dc_metric1 / rev_metric1
        nc_margin = pbt_metric / rev_metric
        nc_margin1 = pbt_metric1 / rev_metric1

        html_line="""<hr style="display: block; margin-top:0.2em; margin-bottom:0.2em; margin-left:auto; margin-right:auto; border-style:inset; border-width:2.5px;"></h1>"""
        st.markdown(html_line, unsafe_allow_html=True)
        kpi1, kpi2, kpi3, kpi4, kpi5, kpi6, kpi7, kpi8 = st.columns(8)
        kpi1.metric(label = "Trips", value = int(trip_metric), delta = int(trip_metric - trip_metric1))
        kpi2.metric(label = "Revenue", value = millify(int(rev_metric), precision=2), delta = millify(int(rev_metric - rev_metric1), precision=2))
        kpi3.metric(label = "Gross Contribution", value = millify(int(dc_metric), precision=2), delta = millify(int(dc_metric - dc_metric1), precision=2))
        kpi4.metric(label = "Net Contribution", value = millify(int(nc_metric), precision=2), delta = millify(int(nc_metric - nc_metric1), precision=2))
        kpi5.metric(label = "EBITDA", value = millify(int(ebita_metric), precision=2), delta = millify(int(ebita_metric - ebita_metric1), precision=2))
        kpi6.metric(label = "PBT", value = millify(int(pbt_metric), precision=2), delta = millify(int(pbt_metric - pbt_metric1), precision=2))
        kpi7.metric(label = "Gross Profit Margin", value = "%.2f" %dc_margin, delta = "%.2f" %(dc_margin - dc_margin1))
        kpi8.metric(label = "Net Profit Margin", value = "%.2f" %nc_margin, delta = "%.2f" %(nc_margin - nc_margin1))
        st.markdown(html_line, unsafe_allow_html=True)

        ### BAR PLOT ######
        account_type = st.selectbox("Account Item", display_data(quarterly_data, units).T.columns.tolist())
        v1 = display_data(quarterly_data, units).T[account_type].values.tolist()
        attr = [i for i in display_data(quarterly_data, units)]#.T.loc["Revenue"].index.format()]

        b = (Bar()
            .add_xaxis(attr)
            .add_yaxis(account_type, v1)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="Monthly Trends", subtitle="2016-2018 Trends in GHS '000 except Trips")))
        st_pyecharts(b)

        value1 = display_data(quarterly_data, units).T[account_type][:4].values.tolist()
        value2 = display_data(quarterly_data, units).T[account_type][4:8].values.tolist()
        value3 = display_data(quarterly_data, units).T[account_type][8:12].values.tolist()
        attribute1 = ["Q1", "Q2", "Q3", "Q4"]

        c = (Bar()
            .add_xaxis(attribute1)
            .add_yaxis("2016", value1)
            .add_yaxis("2017", value2)
            .add_yaxis("2018", value3)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="2016-2018 Monthly Comparison", subtitle=account_type+" Comparison for "+units)))
        st_pyecharts(c)

        data_show = st.checkbox('Show Data')
        if data_show:
            display_df(quarterly_data, units)

else:
    def business_wise():
        rev_metric = display_data(annual_data, units).T.iloc[-1].loc[units + " Revenue"]
        rev_metric1 = display_data(annual_data, units).T.iloc[-2].loc[units + " Revenue"]
        dc_metric = display_data(annual_data, units).T.iloc[-1].loc[units + " GC"]
        dc_metric1 = display_data(annual_data, units).T.iloc[-2].loc[units + " GC"]
        nc_metric = display_data(annual_data, units).T.iloc[-1].loc[units + " NC"]
        nc_metric1 = display_data(annual_data, units).T.iloc[-2].loc[units + " NC"]
        ebita_metric = display_data(annual_data, units).T.iloc[-1].loc[units + " EBITA"]
        ebita_metric1 = display_data(annual_data, units).T.iloc[-2].loc[units + " EBITA"]
        pbt_metric = display_data(annual_data, units).T.iloc[-1].loc[units + " PBT"]
        pbt_metric1 = display_data(annual_data, units).T.iloc[-2].loc[units + " PBT"]
        trip_metric = display_data(annual_data, units).T.iloc[-1].loc[units + " Trips"]
        trip_metric1 = display_data(annual_data, units).T.iloc[-2].loc[units + " Trips"]
        km_metric = display_data(annual_data, units).T.iloc[-1].loc[units + " Distance"]
        km_metric1 = display_data(annual_data, units).T.iloc[-2].loc[units + " Distance"]
        dc_margin = dc_metric / rev_metric
        dc_margin1 = dc_metric1 / rev_metric1
        nc_margin = pbt_metric / rev_metric
        nc_margin1 = pbt_metric1 / rev_metric1

        html_line="""<hr style="display: block; margin-top:0.2em; margin-bottom:0.2em; margin-left:auto; margin-right:auto; border-style:inset; border-width:2.5px;"></h1>"""
        st.markdown(html_line, unsafe_allow_html=True)
        kpi1, kpi2, kpi3, kpi4, kpi5, kpi6, kpi7, kpi8 = st.columns(8)
        kpi1.metric(label = "Trips", value = int(trip_metric), delta = int(trip_metric - trip_metric1))
        kpi2.metric(label = "Revenue", value = millify(int(rev_metric), precision=2), delta = millify(int(rev_metric - rev_metric1), precision=2))
        kpi3.metric(label = "Gross Contribution", value = millify(int(dc_metric), precision=2), delta = millify(int(dc_metric - dc_metric1), precision=2))
        kpi4.metric(label = "Net Contribution", value = millify(int(nc_metric), precision=2), delta = millify(int(nc_metric - nc_metric1), precision=2))
        kpi5.metric(label = "EBITDA", value = millify(int(ebita_metric), precision=2), delta = millify(int(ebita_metric - ebita_metric1), precision=2))
        kpi6.metric(label = "PBT", value = millify(int(pbt_metric), precision=2), delta = millify(int(pbt_metric - pbt_metric1), precision=2))
        kpi7.metric(label = "Gross Profit Margin", value = "%.2f" %dc_margin, delta = "%.2f" %(dc_margin - dc_margin1))
        kpi8.metric(label = "Net Profit Margin", value = "%.2f" %nc_margin, delta = "%.2f" %(nc_margin - nc_margin1))
        st.markdown(html_line, unsafe_allow_html=True)

        ### BAR PLOT ######
        account_type = st.selectbox("Account Item", display_data(annual_data, units).T.columns.tolist())
        v1 = display_data(annual_data, units).T[account_type].values.tolist()
        attr = [i for i in display_data(annual_data, units)]#.T.loc["Revenue"].index.format()]

        b = (Bar()
            .add_xaxis(attr)
            .add_yaxis(account_type, v1)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="Monthly Trends", subtitle="2016-2018 Trends in GHS '000 except Trips")))
        st_pyecharts(b)

        value1 = display_data(annual_data, units).T[account_type][:1].values.tolist()
        value2 = display_data(annual_data, units).T[account_type][1:2].values.tolist()
        value3 = display_data(annual_data, units).T[account_type][2:3].values.tolist()
        attribute1 = ["Year"]

        c = (Bar()
            .add_xaxis(attribute1)
            .add_yaxis("2016", value1)
            .add_yaxis("2017", value2)
            .add_yaxis("2018", value3)
            .set_series_opts(label_opts=opts.LabelOpts(is_show=False))
            .set_global_opts(title_opts=opts.TitleOpts(title="2016-2018 Monthly Comparison", subtitle=account_type+" Comparison for "+units)))
        st_pyecharts(c)

        data_show = st.checkbox('Show Data')
        if data_show:
            display_df(annual_data, units)

    
    

business_wise()
