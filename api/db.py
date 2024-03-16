from typing import Any, Dict, List, Tuple, Union

import pymysql

# Type definitions
# Key-value pairs
KV = Dict[str, Any]
# A Query consists of a string (possibly with placeholders) and a list of values to be put in the placeholders
Query = Tuple[str, List]

class DB:
	def __init__(self, host: str, port: int, user: str, password: str, database: str):
		conn = pymysql.connect(
			host=host,
			port=port,
			user=user,
			password=password,
			database=database,
			cursorclass=pymysql.cursors.DictCursor,
			autocommit=True,
		)
		self.conn = conn

	def get_cursor(self):
		return self.conn.cursor()

	def execute_query(self, query: str, args: List, ret_result: bool) -> Union[List[KV], int]:
		"""Executes a query.

		:param query: A query string, possibly containing %s placeholders
		:param args: A list containing the values for the %s placeholders
		:param ret_result: If True, execute_query returns a list of dicts, each representing a returned
							row from the table. If False, the number of rows affected is returned. Note
							that the length of the list of dicts is not necessarily equal to the number
							of rows affected.
		:returns: a list of dicts or a number, depending on ret_result
		"""
		cur = self.get_cursor()
		count = cur.execute(query, args=args)
		if ret_result:
			return cur.fetchall()
		else:
			return count


	# TODO: all methods below

	# Yes, in Python, you can call a static method from both the class itself and an instance of the class.
	@staticmethod
	def build_select_query(table: str, rows: List[str], filters: KV) -> Query:
		"""Builds a query that selects rows. See db_test for examples.

		:param table: The table to be selected from
		:param rows: The attributes to select. If empty, then selects all rows.
		:param filters: Key-value pairs that the rows from table must satisfy
		:returns: A query string and any placeholder arguments
		"""
		select_string = f"SELECT {', '.join(rows) if len(rows)!=0 else '*'} FROM {table}"
		filter_string = " WHERE " + " AND ".join([f'{key} = %s' for key, value in filters.items()]) if len(filters) != 0 else ""
		filter_list = [v for k, v in filters.items()]
		query_string = select_string + filter_string
		return query_string, filter_list

	def select(self, table: str, rows: List[str], filters: KV) -> List[KV]:
		"""Runs a select statement. You should use build_select_query and execute_query.

		:param table: The table to be selected from
		:param rows: The attributes to select. If empty, then selects all rows.
		:param filters: Key-value pairs that the rows to be selected must satisfy
		:returns: The selected rows
		"""
		my_query, args = self.build_select_query(table, rows, filters)
		return self.execute_query(my_query, args, True)



	@staticmethod
	def build_insert_query(table: str, values: KV) -> Query:
		"""Builds a query that inserts a row. See db_test for examples.

		:param table: The table to be inserted into
		:param values: Key-value pairs that represent the values to be inserted
		:returns: A query string and any placeholder arguments
		"""
		query_string = f"INSERT INTO {table} ({f', '.join([k for k,v in values.items()])}) VALUES ({f', '.join(['%s' for k,v in values.items()])})"
		return query_string, [v for k,v in values.items()]

	def insert(self, table: str, values: KV) -> int:
		"""Runs an insert statement. You should use build_insert_query and execute_query.

		:param table: The table to be inserted into
		:param values: Key-value pairs that represent the values to be inserted
		:returns: The number of rows affected
		"""
		query, args = self.build_insert_query(table, values)
		return self.execute_query(query, args, True)

	@staticmethod
	def build_update_query(table: str, values: KV, filters: KV) -> Query:
		"""Builds a query that updates rows. See db_test for examples.

		:param table: The table to be updated
		:param values: Key-value pairs that represent the new values
		:param filters: Key-value pairs that the rows from table must satisfy
		:returns: A query string and any placeholder arguments
		"""
		# "UPDATE student SET name = %s, dept_name = %s, tot_cred = %s WHERE name = %s AND dept_name = %s"
		update_clause = f"UPDATE {table} SET {', '.join([k + f' = %s' for k,v in values.items()])}"
		where_clause = f" WHERE {' AND '.join([k + f' = %s' for k,v in filters.items()])}" if len(filters) > 0 else ""
		full_update = update_clause + where_clause
		return full_update, [v for k,v in values.items()]+[v for k,v in filters.items()]

	def update(self, table: str, values: KV, filters: KV) -> int:
		"""Runs an update statement. You should use build_update_query and execute_query.

		:param table: The table to be updated
		:param values: Key-value pairs that represent the new values
		:param filters: Key-value pairs that the rows to be updated must satisfy
		:returns: The number of rows affected
		"""
		query, args = self.build_update_query(table, values, filters)
		return self.execute_query(query, args, True)


	@staticmethod
	def build_delete_query(table: str, filters: KV) -> Query:
		"""Builds a query that deletes rows. See db_test for examples.

		:param table: The table to be deleted from
		:param filters: Key-value pairs that the rows to be deleted must satisfy
		:returns: A query string and any placeholder arguments
		"""
		# "DELETE FROM student WHERE ID = %s AND name = %s"
		delete_clause = f"DELETE FROM {table}"
		where_clause = f" WHERE {' AND '.join([k + ' = %s' for k,v in filters.items()])}" if len(filters) > 0 else ""
		return delete_clause + where_clause, [v for k,v in filters.items()]

	def delete(self, table: str, filters: KV) -> int:
		"""Runs a delete statement. You should use build_delete_query and execute_query.

		:param table: The table to be deleted from
		:param filters: Key-value pairs that the rows to be deleted must satisfy
		:returns: The number of rows affected
		"""
		query, args = self.build_delete_query(table, filters)
		return self.execute_query(query, args, True)