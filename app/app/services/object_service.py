class ObjectService:

    @staticmethod
    def get_objects(date=None, object_type=None, orbit=None):
        # TODO: query tracked_objects JOIN orbital_snapshots
        # TODO: apply filters — date, object_type (PAYLOAD/DEBRIS/ROCKET_BODY/UNKNOWN), orbit (LEO/MEO/GEO)
        # TODO: return list of dicts: [{norad_id, name, lat, lon, altitude_km, object_type, orbit}, ...]
        pass

    @staticmethod
    def get_object_detail(norad_id: int):
        # TODO: query tracked_objects for this norad_id
        # TODO: include last N orbital_snapshots (tle_line1, tle_line2, inclination, etc.)
        # TODO: return dict or None if not found
        pass
