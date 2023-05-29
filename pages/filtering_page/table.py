import sqlite3
import pandas as pd


conn = sqlite3.connect('master.db')

full_df = pd.read_sql_query(
    '''
        SELECT 
            s.id_sale, 
            s.date, 
            ifnull(s.date2, 'Н/Д') date2,
            ifnull(m.location || ' - ' || m.name_market, 'Н/Д') market,
            ifnull(br.name_actor || ' ('|| br.type ||')', 'Н/Д') buyer,
            ifnull(sr.name_actor || ' ('|| sr.type ||')', 'Н/Д') seller,
            ifnull(i.name  || ' ('|| i.measure ||')', 'Н/Д') item,
            ifnull(p.location || ' - ' || p.name_production, 'Н/Д') production,
            s.amount,
            s.cost,
            round(s.cost / s.amount, 1) price,
			ifnull(name_archive || ', Ф. ' || fund || ', Оп. ' || inventory || ', д. ' || storage_unit || ', "' || name_source || '"', 'Н/Д') source,
            ifnull(s.page, 'Н/Д') page
        from Sales s
        join Items i on s.fid_item = i.id_item
        join Production p on s.fid_production = p.id_production
        left join Actors br on s.fid_buyer = br.id_actor
        left join Actors sr on s.fid_seller = sr.id_actor
        join Markets m on s.fid_market = m.id_market
        join Sources src on s.fid_source = src.id_source
        join Storage st on src.fid_storage = st.id_storage
        join Archives a on st.fid_archive = a.id_archive
    ''', 
    conn
)

conn.close()