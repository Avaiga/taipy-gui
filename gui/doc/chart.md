Displays data sets in a chart or a group of charts.

The chart control is based on the [plotly.js](https://plotly.com/javascript/)
graphs library.

<style>
.h2 {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.h2 a{
  font-weight: 400;
  font-size: 16px;
  line-height: 24px;
  display: flex;
  align-items: center;
}
.h2 a svg{
    fill: #FE462B;
    max-height: 100%;
    width: 1.125em;
    margin-right: 10px;
}
.list{
    display: flex;
    justify-content: space-between;
    list-style: none;
    gap: 16px;
    padding: 0;
}
.list li{
    margin: 0 !important;
    padding: 0;
    width:171px;
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 16px;
    gap: 16px;
    background: #191622;
    border-radius: 4px;
}
.list a{
    font-size: 14px;
    line-height: 17px;
    color: #FFFFFF;
    display: flex;
    justify-content: space-between;
    align-items: center;
    width: 100%;
}
.list a svg{
    fill: #FE462B;
    max-height: 100%;
    width: 1.125em;
    margin-left: 10px;
}
</style>

<h2 class='h2'>Basic charts <a href='#'><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg> More basic charts</a></h2>
<ul class='list'>
    <li>
        <img src='./chart-assets/scatter-plots.png' />
        <a href='#'>Scatter plots <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/line-charts.png' />
        <a href='#'>Line charts <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/bar-charts.png' />
        <a href='#'>Bar charts <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/pie-charts.png' />
        <a href='#'>Pie charts <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/bubble-charts.png' />
        <a href='#'>Bubble charts <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
</ul>

<h2 class='h2'>Statistical charts <a href='#'><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg> More  statistical charts</a></h2>
<ul class='list'>
    <li>
        <img src='./chart-assets/error-bars.png' />
        <a href='#'>Error Bars <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/box-plots.png' />
        <a href='#'>Box plots <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/histograms.png' />
        <a href='#'>Histograms <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/distplots.png' />
        <a href='#'>Distplots <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/2D-histograms.png' />
        <a href='#'>2D histograms <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
</ul>

<h2 class='h2'>Scientific charts <a href='#'><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg> More  scientific charts</a></h2>
<ul class='list'>
    <li>
        <img src='./chart-assets/contour-plots.png' />
        <a href='#'>Contour plots <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/heatmaps.png' />
        <a href='#'>Heatmaps <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/imshow.png' />
        <a href='#'>Imshow <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/ternary-plots.png' />
        <a href='#'>Ternary plots <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/log-plots.png' />
        <a href='#'>Log plots <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
</ul>

<h2 class='h2'>Financial charts <a href='#'><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg> More  financial charts</a></h2>
<ul class='list'>
    <li>
        <img src='./chart-assets/time-series&date-axes.png' />
        <a href='#'>Time series & date axes <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/candlestick-charts.png' />
        <a href='#'>Candlestick charts <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/waterfall-charts.png' />
        <a href='#'>Waterfall charts <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/funnel-charts.png' />
        <a href='#'>Funnel charts <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/OHLC-charts.png' />
        <a href='#'>OHLC charts <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
</ul>

<h2 class='h2'>Maps <a href='#'><svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg> More  maps</a></h2>
<ul class='list'>
    <li>
        <img src='./chart-assets/mapbox-choropleth-maps.png' />
        <a href='#'>Mapbox Choropleth maps <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/lines-on-mapbox.png' />
        <a href='#'>Lines on Mapbox <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/filled-area-on-maps.png' />
        <a href='#'>Filled area on Maps <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/bubble-maps.png' />
        <a href='#'>Bubble maps <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
    <li>
        <img src='./chart-assets/mapbox-density-heatmap.png' />
        <a href='#'>Mapbox density heatmap <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24"><path d="M4 11v2h12l-5.5 5.5 1.42 1.42L19.84 12l-7.92-7.92L10.5 5.5 16 11H4z"></path></svg></a>
    </li>
</ul>

## Properties

A chart control can hold several traces, that can display individual data sets.

To indicate properties for a given trace, you will use the indexed properties
(using the *property_name[index]* syntax, with the indices starting at index 1) to
specify which trace you target.

Indexed properties can have a default value (using the *property_name* syntax with
no index) which is overridden by any specified indexed property.

The _data_ property supported types are:

- pandas Dataframe
- list of lists
- numpy series
- list of pandas dataframes



## Usage

- [Basic concepts](charts/basics.md)
- [Other features](charts/others.md)
