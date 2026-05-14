# services/aggregation.py

BASE_QUERY = """
SELECT
  cr.employee_id,

  ROUND(SUM(
    CASE 
      WHEN (strftime('%s', cr.clock_in) - strftime('%s', c.shift_start)) > 0
      THEN (strftime('%s', cr.clock_in) - strftime('%s', c.shift_start)) / 3600.0
      ELSE 0
    END
  ), 2) AS late_hours,

  ROUND(SUM(
    CASE 
      WHEN (strftime('%s', cr.clock_out) - strftime('%s', c.shift_end)) > 0
      THEN (strftime('%s', cr.clock_out) - strftime('%s', c.shift_end)) / 3600.0
      ELSE 0
    END
  ), 2) AS overtime_hours,

  ROUND(SUM(
    CASE 
      WHEN (strftime('%s', cr.clock_in) - strftime('%s', c.shift_start)) > 0
      THEN (strftime('%s', cr.clock_in) - strftime('%s', c.shift_start)) / 3600.0
      ELSE 0
    END
    * c.late_cut_rate
  ), 2) AS total_late_cut,

  ROUND(SUM(
    CASE 
      WHEN (strftime('%s', cr.clock_out) - strftime('%s', c.shift_end)) > 0
      THEN (strftime('%s', cr.clock_out) - strftime('%s', c.shift_end)) / 3600.0
      ELSE 0
    END
    * c.overtime_rate
  ), 2) AS total_overtime_pay

FROM clock_records cr
JOIN configs c ON cr.employee_type = c.employee_type
"""