def parse_name(name):
    hash = {
        "DT_MEDICAO": 'Date',
        "TEM_MAX": 'Tmax',
        "TEM_MIN": 'Tmin',
        "UMD_MAX": 'RHmax',
        "UMD_MIN": 'RHmin',
        "PRE_INS": 'P',
        "VEN_VEL": 'u2',
        "RAD_GLO": 'Rn',
        "CHUVA": 'PREC',
        "VL_LATITUDE": 'Latitude',
        "VL_LONGITUDE": 'Longitude'
    }
    return hash.get(name)

def isnumber(value):
    return value.replace(".","").replace("-","",1).isnumeric()
