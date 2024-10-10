import random


class MinuteInterval:
    """
    Class representing a minute interval within a 24-hour period.

    This class is used to define an interval in minutes, providing functionality to generate random minutes
    within that interval, check if a specific minute falls within the interval, and access the start and end
    points of the interval.

    Attributes:
        _start (int): The starting minute of the interval (0-1439).
        
        _end (int): The ending minute of the interval (0-1439).

    Methods:
        random() -> int:
            Generates a random minute within the defined interval.
        
        start_minute() -> int:
            Returns the starting minute of the interval.
        
        end_minute() -> int:
            Returns the ending minute of the interval.
        
        contains(minute: int) -> bool:
            Checks if a given minute is within the defined interval.
    """
    def __init__(self,start:float,end:float,inHours:bool=False):
        """
        Initializes a MinuteInterval instance. Includes start, excludes end

        Args:
            start (float): The start of the interval in minutes (or hours if inHours is True). 
            end (float): The end of the interval in minutes (or hours if inHours is True).
            inHours (bool, optional): Flag indicating if the provided start and end are in hours. Defaults to False.

        Raises:
            ValueError: If start or end are not between 0 and 1440 minutes.
        """
        if inHours:
            start=int(start*60)
            end=int(end*60)
        if start>1440 or end>1440: raise ValueError("Sart and end have to be between 00:00 and 24:00")
        self._start=start
        self._end=end
    
    def random(self)->int:
        """
        Generates a random minute within the defined interval.

        Returns:
            int: A random minute within the interval, which is inclusive of the start and exclusive of the end.
        """
        if self._start < self._end:
            return random.randint(self._start, self._end - 1)
        else:
            length_first_range = 1440 - self._start
            length_second_range = self._end
            total_length = length_first_range + length_second_range
            random_index = random.randint(0, total_length - 1)
            if random_index < length_first_range:
                return self._start + random_index
            else:
                return random_index - length_first_range
            
    def start_minute(self):
        """
        Returns the starting minute of the interval.

        Returns:
            int: The starting minute of the interval.
        """
        return self._start
    
    def end_minute(self):
        """
        Returns the ending minute of the interval.

        Returns:
            int: The ending minute of the interval.
        """
        return self._end
    
    def contains(self,minute):
        """
        Checks if a given minute is within the defined interval.

        Args:
            minute (int): The minute to check.

        Returns:
            bool: True if the minute is within the interval, False otherwise.
        """
        if self._start<=self._end:
            if minute>=self._start and minute<self._end: return True
            else: return False
        else:
            if minute>self._end and minute<self._start: return False
            else: return True



