# **🧾 Nota Metodológica**

## **Fuentes**

Los datos utilizados en esta aplicación provienen de fuentes oficiales. Las cifras de homicidios corresponden al año 2024 y fueron tomadas de la Policía Nacional de Colombia a través de su sistema de estadística delictiva. Para el denominador de la tasa se emplearon las proyecciones de población del DANE para 2024, utilizando como referencia la población media del año según los supuestos oficiales. Asimismo, se incorporó el catálogo DIVIPOLA del DANE como clave de unión para garantizar consistencia en los cruces de información, y se usó la cartografía oficial del DANE (en formato parquet) para la visualización geográfica. La fecha de corte de la información es del 31 de diciembre del año 2024.

## **Estimación de la Tasa de Homicidios Muncipal**

En cuanto a la metodología, la tasa municipal de homicidios se estimó relacionando el total de homicidios ocurridos en cada municipio con la población proyectada del mismo municipio, multiplicado por 100.000 habitantes. Se asumió como válida la población media de las proyecciones oficiales y se aplicó el catálogo DANE (DIVIPOLA) para mantener uniformidad territorial en los datos.

## **Descripción de la App**

La aplicación desarrollada permite analizar el fenómeno de los homicidios en Colombia durante el año 2024 a través de diferentes enfoques visuales e interactivos. En primer lugar, se presentan indicadores agregados como el total de homicidios registrados y la tasa promedio nacional por cada 100.000 habitantes. Posteriormente, se realiza un análisis departamental mediante un gráfico de barras que muestra la distribución de los homicidios totales por departamento, lo que facilita la comparación entre las regiones del país. A nivel municipal, se incluye un gráfico de barras que presenta las tasas de homicidios por municipio, resaltando aquellos con las cifras más elevadas, así como un ranking comparativo que contrasta los 10 municipios con mayores tasas frente a los 10 con menores tasas, lo que ofrece una visión clara. Finalmente, un mapa de calor plano que permite visualizar de manera espacial la concentración de homicidios a nivel municipal y departamental, evidenciando patrones geográficos clave. En conjunto, estas visualizaciones facilitan la comprensión de la magnitud, distribución y diferencias territoriales de los homicidios en Colombia, constituyéndose en una herramienta útil para el análisis académico y la toma de decisiones en política pública.
 

## **Limitaciones**

El análisis enfrenta algunas limitaciones relevantes. En primer lugar, existe la posibilidad de subregistro, ya que por falencias operativas algunos no se registran. En segundo lugar, los cambios territoriales derivados de modificaciones en la división político-administrativa pueden afectar la comparabilidad en el tiempo. En tercer lugar, las tasas presentan alta volatilidad en municipios pequeños, debido a que ligeras variaciones en los homicidios generan desviaciones extremas en el calculo del indicador. Finalmente, la información depende en su totalidad de fuentes oficiales (Policía Nacional y DANE) y no contempla posibles ajustes posteriores a la fecha de corte. A demás, los datos de población puede que no sean precisos, ya que su estimación es realizada por medio de proyecciones bajo el supuesto de que su crecimiento es constante, sin embargo, no se tienen factores externos en cuenta que afectan esta variable.

## **🖥️ Link App ->** https://homicidios.streamlit.app/
