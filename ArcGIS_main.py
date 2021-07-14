import time
from arcgis.gis import GIS
from arcgis.features import FeatureLayer
from passwordManager import u, p
import random
import string
import database_writer
import Send_Email
from html_proveit import html_email
import chime


def update_and_submit():
    query_result1.features[index].attributes['processed'] = 'Processing'
    query_result1.features[index].attributes['search_id'] = id_gen
    flayer.edit_features(updates=query_result1.features)
    print(index, easting, northing, creator, 'search submitted')


def id_generator(size=10, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


while True:
    try:
        gis = GIS(username=u, password=p)
        search_results = gis.content.search('title: New_STATS_Requests',
                                            'Feature Layer')
        while True:
            l1 = search_results[2]
            l1 = l1.layers
            flayer = l1[0]
            query_result1 = flayer.query(where='processed IS NULL', out_sr=27700)
            print(len(query_result1.features), 'features')
            time.sleep(5)
            flayer_rows = query_result1.sdf

            for index, row in flayer_rows.iterrows():
                chime.success()  # dings when new search is found
                id_gen = id_generator()
                easting = row['SHAPE']['x']

                northing = row['SHAPE']['y']

                creator = row['Creator']

                email_address = row['email']

                ref = row['reference']

                contract = row['contract']

                if row['processed'] is None:
                    try:
                        url = f'https://services2.arcgis.com/4mdxlPzHnZKtJJX9/arcgis/rest/services/OSGB_500m_Grids/FeatureServer/0/query?where=1%3D1&text=&objectIds=&time=&geometry={easting}%2C+{northing}&geometryType=esriGeometryPoint&inSR=27700&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=27700&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&returnTrueCurves=false&resultOffset=&resultRecordCount=&f=pjson'
                        url_HE = f'https://services2.arcgis.com/4mdxlPzHnZKtJJX9/arcgis/rest/services/HE_proveit/FeatureServer/0/query?where=1%3D1&text=&objectIds=&time=&geometry={easting}%2C+{northing}&geometryType=esriGeometryPoint&inSR=27700&spatialRel=esriSpatialRelIntersects&relationParam=&outFields=*&returnGeometry=true&maxAllowableOffset=&geometryPrecision=&outSR=27700&returnIdsOnly=false&returnCountOnly=false&orderByFields=&groupByFieldsForStatistics=&outStatistics=&returnZ=false&returnM=false&gdbVersion=&returnDistinctValues=false&returnTrueCurves=false&resultOffset=&resultRecordCount=&f=pjson&'
                        if contract[0:2].upper() == 'HE':
                            layer = FeatureLayer(gis=gis, url=url_HE)
                            tile_name = str(layer.properties.features[0]['attributes']['topo_ref'])
                        else:
                            layer = FeatureLayer(url)
                            tile_name = str(layer.properties.features[0]['attributes']['TILE_NAME'])
                        print(tile_name, email_address, contract)

                        update_and_submit()
                        database_writer.insert_search_row(id_gen, email_address, creator, tile_name, round(easting),
                                                           round(northing), ref, contract)

                    except Exception as e:
                        print(e)

                        objid = query_result1.features[index].get_value('objectid')
                        print(objid)
                        Send_Email.send_email(email_recipient=email_address, email_subject='ProveIT STATS',
                                              email_message=f'Hello {creator},\n\nSomething has gone wrong with your submission. Please try again\n\n{html_email(ref)}')
                        query_result1.features[index].attributes['processed'] = 'Invalid Search'
                        flayer.edit_features(updates=query_result1.features)
                        # flayer.edit_features(deletes=str(objid))  # feature will be deleted if out of range
    except Exception as e:
        print(e)
        time.sleep(30)
