from .. import execute_query
from datetime import datetime, date

class SmEpolModel:

    def read_training_summary_report(self, year = None):
        query = "SELECT course_name,course_code, MONTH(training_dt_enrolled) AS MONTH, "
        query += "(CASE WHEN course_code LIKE 'ePembekal-%' THEN 'Supplier' "
        query +=  "WHEN course_code LIKE 'ePTJ-%' THEN 'PTJ' "
        query +=  "ELSE course_code "
        query += "END) AS type_user, "
        query += "COUNT(*) AS total "
        query += "FROM epol_training "
        query += "WHERE   YEAR(training_dt_enrolled) = '{}' ".format(year if year is not None else datetime.now().year)
        query += "AND course_type = 'ePembelajaran' "
        query += "AND ( course_code LIKE 'ePembekal-%' OR course_code LIKE 'ePTJ-%') "
        query += "GROUP BY   course_name, course_code  , MONTH(training_dt_enrolled) "         
        query += "ORDER BY course_code,3 "
        return execute_query(query)