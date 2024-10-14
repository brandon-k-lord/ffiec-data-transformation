/*
 * Functions for cleaning and transforming FFIEC data
 * 
 * DESCRIPTION: 
 * This file specifically for the creation of functions.
 * 
 * DEPENDENCIES:
 * - setting search_path = 'transformations'
 *
 * */


set search_path = 'transformations';

/*
 * DESCRIPTION:
 * Dynamic sql function returning a list of column in a specified table that contains whitespace where it is not expected.
 * 
 * INTENT:
 * - Output == columns that contain whitespace where we do not expect given a specified table.
 * - Limited to data type varchar
 * 
 * INPUT:
 * - [input_schema_table_name] == [table_schema].[table_name]
 * - example == 'transformations.tmp_table'
 * - notice it expects text input and requires to be in quotations
 * 
 * */


create or replace function col_w_whitespace(input_schema_table_name text)
returns table(column_name text,record_count int) as $$
declare 
	input_table_name text;
	input_schema text;
	input_table text;
	input_data_type text;	
	sql_query text;	
	rec record;
	result_count int;	
	
begin
	input_schema := split_part(input_schema_table_name,'.',1);
	input_table := split_part(input_schema_table_name,'.',2);
	input_data_type := 'character varying';	

	raise notice 'table_schema: %',input_schema;
	raise notice 'table: %',input_table;
	raise notice 'data_type: %', input_data_type;

	for rec in 
		select cols.column_name
		from information_schema.columns cols
		where 
			cols.table_schema = input_schema
		and 
			cols.table_name = input_table
		and 
			cols.data_type = input_data_type
	loop
		raise notice  'Column name: %', rec.column_name;
		sql_query := format(
			'select count(*) from %I where length(%I) <> length(trim(%I))',
			input_table,
			rec.column_name,
			rec.column_name
		);
		execute sql_query into result_count;
		if result_count > 0 then
			raise notice 'column: %s',rec.column_name;
			raise notice 'record_count: %s', result_count;
			return query select rec.column_name::text, result_count;
		end if;
	end loop;
	return;
end; 
$$ language plpgsql;


/*
 * DESCRIPTION:
 * Dynamic sql function to remove whitespace for a specified column list.
 * Conservative approach was taken to utilize a specified list for more flexibiliy and control.
 * 
 * INTENT:
 * - Output == columns striped of whitespace.
 * - Limited to specified columns
 * - includes a result set output attributes of column, rows_affected
 * 
 * INPUT:
 * - [input_schema_table_name] == [table_schema].[table_name]
 * - example == 'transformations.tmp_table'
 * - notice it expects text input and requires to be in quotations
 * 
 * - input_list[] == ['column1', 'column2']
 * - exmaple == ['first_name', 'last_name']
  * 
 * */


create or replace function rm_col_whitespace( input_schema_table text, input_list text[])
returns table(column_name text,record_count int) as $$
declare
	item text;
	sql_stm text;
	row_count int;
		
begin 
	raise notice 'procesing table: %', input_schema_table;
	foreach item in array input_list
	loop
		raise notice 'procesing column: %', item;
		sql_stm := format(
		'update %I set %I = trim(%I)',
		input_schema_table,
		item,
		item
		);
		raise notice 'executing query: %',sql_stm;
		execute sql_stm;
		get diagnostics row_count = ROW_COUNT;
		raise notice 'update_results  |  column: %  |  rows_updated: %',item, row_count;
		return query select item, row_count;
	end loop;
		
	return;
end; $$
language plpgsql;