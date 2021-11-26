from .tile import *

class Hallway:
	"""
	Data representation of an individual hallway for the game Snarl.

	For hallways to be valid there needs:
		- Start position not equal to  end position, 
		- Given start pos, end pos, and waypoints are valid Position2d
		- Vertical or horizontal lines connect each point
		- Each way point is a corner

	Parameters
	----------
	start_pos : tuple
		row and column index of the start tile
	end_pos : tuple
		row and column index of the end tile
	waypoints : List[tuple], default []
		List of row and column indices for each waypoint in the hallway where there is a corner
	"""
	def __init__(self, start_pos, end_pos, waypoints=[]):
		# Ensure hallway does not start and end on same tile
		if start_pos == end_pos:
			raise ValueError("Hallway cannot start and stop on same tile.")
			
		for point in ([start_pos, end_pos] + waypoints):
			if len(point) != 2 or point[0] < 0 or point[1] < 1:
				raise ValueError(f"{point} is an invalid coordinate.")

		self._start_pos = start_pos
		self._end_pos = end_pos
		self._waypoints = waypoints
		self._validate_points()
		self._all_tiles = self._build_all_tiles()
		self._max_width = 0
		self._max_height = 0
		self._calculate_dimensions()	


	def _validate_points(self):
		"""
		Ensure that there is no diagonal halls in the level and that each waypoint is a corner
		"""
		polyline = [self._start_pos] + self._waypoints + [self._end_pos]
		
		for ind in range(1, len(polyline)):
			prev_point = polyline[ind - 1]
			point = polyline[ind]

			# Diagonal line between waypoints
			if not (point[0] == prev_point[0] or point[1] == prev_point[1]):
				raise ValueError(f"Hallway is not straight between {point} and {prev_point}")
			# Way point that is not a corner
			if ind != len(polyline) - 1 and (
				(prev_point[0] == point[0] == polyline[ind+1][0]) or
				(prev_point[1] == point[1] == polyline[ind+1][1])):
				raise ValueError(f"Waypoint {point} is not a corner.")

	def _build_all_tiles(self):
		"""
		Generate a list of tiles for each point in the hallway. Not including start and end points.

		Returns
		-------
		List[Tile]
			List of all tiles that make up the hallway
		"""
		polyline = [self._start_pos] + self._waypoints + [self._end_pos]
		all_points = []

		for ind in range(1, len(polyline)):
			prev_point = polyline[ind - 1]
			point = polyline[ind]
			# Vertical line connecting points
			if prev_point[1] == point[1]:
				top = min(prev_point[0], point[0])
				bottom = max(prev_point[0], point[0])
				for y in range(top + 1, bottom):
					all_points.append((y, point[1]))
			# Horizontal line connecting points
			else:
				leftmost = min(prev_point[1], point[1])
				rightmost = max(prev_point[1], point[1])
				for x in range(leftmost + 1, rightmost):
					all_points.append((point[0], x))

		all_points += self._waypoints
		all_tiles = [Space(pt[0], pt[1]) for pt in all_points]

		for tile in all_tiles:
			if all_tiles.count(tile) > 1:
				raise ValueError('Hallway overlaps with itself.')
		return all_tiles

	def _calculate_dimensions(self):
		"""
		Determine the furthest point along the x and y axis.
		"""
		for point in ([self._start_pos] + self._waypoints + [self._end_pos]):
			if point[0] > self._max_height:
				self._max_height = point[0]
			if point[1] > self._max_width:
				self._max_width = point[1]

	def get_max_width(self):
		"""
		Retrieve the column index of the rightmost point.

		Returns
		-------
		int
			Furthestmost right column index
		"""
		return self._max_width

	def get_max_height(self):
		"""
		Retrieve the column index of the lowest point.

		Returns
		-------
		int
			Bottom-most row index
		"""
		return self._max_height

	def get_start_pos(self):
		"""
		Retrieves the row and col index of the start position of the hallway

		Returns
		-------
		(int,int)
			row and col index of the start position
		"""
		return self._start_pos

	def get_end_pos(self):
		"""
		Retrieves the row and col index of the start position of the hallway

		Returns
		-------
		(int,int)
			row and col index of the start position
		"""
		return self._end_pos


	def get_tiles(self):
		"""
		Retrieves all of the tiles that make up the hallway, not including start and end tiles, where
		where door would be.

		Returns
		-------
		List[Position2D]
			List of all the tiles making up the hallway
		"""
		return self._all_tiles

	def get_JSON(self):
		"""
		Retrieves JSON representation of hallway

		Returns
		-------
		dict
			JSON representation of hallway
		"""
		as_json = {"type": "hallway", "from": self._start_pos, "to": self._end_pos, "waypoints": self._waypoints}
		return as_json






