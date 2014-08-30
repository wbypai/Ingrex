from math import pi,sin,cos,tan,asin,radians,sqrt,log


def fetch_tilekey(lat, lng):
    """
    Return the tile's x, y depend on the latitude and longitude.
    """
    rlat = radians(lat)
    n = 9000
    xtile = int((lng + 180.0) / 360.0 * n)
    ytile = int((1.0 - log(tan(rlat) + (1 / cos(rlat))) / pi) / 2.0 * n)
    return xtile, ytile


def fetch_distence(lat1, lng1, lat2, lng2):
    """
    Return the shortest distence between the two point.
    Unit of Linear Measure : meter.
    """
    lat1, lng1, lat2, lng2 = map(radians, [lat1, lng1, lat2, lng2])
    dlat = lat1 - lat2
    dlng = lng1 - lng2
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlng/2)**2
    c = 2* asin(sqrt(a))
    m = 6367.0 * c * 1000
    return m


def point_in_polygon(x, y, poly):
    """
    poly = [(x1, y1), (x2, y2), (x3, y3), ...]
    if the point (x,y) inside or on the boundary of the polygon, return True
    if the point (x,y) outside of the polygon, return False
    """
    n = len(poly)
    inside = False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside


def transform(wgLat, wgLon):
    """
    transform the latitude and longitude from Earth to Mars
    transform(latitude,longitude) , WGS84
    return (latitude,longitude) , GCJ02
    """
    
    def _outOfChina(lat, lon):
        if (lon < 72.004 or lon > 137.8347):
            return True
        if (lat < 0.8293 or lat > 55.8271):
            return True
        return False
    
    def _transformLat(x, y):
        ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * sqrt(abs(x))
        ret += (20.0 * sin(6.0 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
        ret += (20.0 * sin(y * pi) + 40.0 * sin(y / 3.0 * pi)) * 2.0 / 3.0
        ret += (160.0 * sin(y / 12.0 * pi) + 320 * sin(y * pi / 30.0)) * 2.0 / 3.0
        return ret
    
    def _transformLon(x, y):
        ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * sqrt(abs(x))
        ret += (20.0 * sin(6.0 * x * pi) + 20.0 * sin(2.0 * x * pi)) * 2.0 / 3.0
        ret += (20.0 * sin(x * pi) + 40.0 * sin(x / 3.0 * pi)) * 2.0 / 3.0
        ret += (150.0 * sin(x / 12.0 * pi) + 300.0 * sin(x / 30.0 * pi)) * 2.0 / 3.0
        return ret
    
    a = 6378245.0
    ee = 0.00669342162296594323
    if (_outOfChina(wgLat, wgLon)):
        mgLat = wgLat
        mgLon = wgLon
        return
    dLat = _transformLat(wgLon - 105.0, wgLat - 35.0)
    dLon = _transformLon(wgLon - 105.0, wgLat - 35.0)
    radLat = wgLat / 180.0 * pi
    magic = sin(radLat)
    magic = 1 - ee * magic * magic
    sqrtMagic = sqrt(magic)
    dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * pi)
    dLon = (dLon * 180.0) / (a / sqrtMagic * cos(radLat) * pi)
    mgLat = wgLat + dLat
    mgLon = wgLon + dLon
    return mgLat,mgLon


