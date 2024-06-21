import random


#saves a minute interval, includes start, excludes end
class MinuteInterval:
    def __init__(self,start:int,end:int,inHours:bool=False):
        #start end in minutes if inHours=False
        if inHours:
            start=start*60
            end=end*60
        if start>1440 or end>1440: raise ValueError("Sart and end have to be between 00:00 and 24:00")
        self.start=start
        self.end=end
    
    def random(self)->int:
        if self.start < self.end:
            return random.randint(self.start, self.end - 1)
        else:
            length_first_range = 1440 - self.start
            length_second_range = self.end
            total_length = length_first_range + length_second_range
            random_index = random.randint(0, total_length - 1)
            if random_index < length_first_range:
                return self.start + random_index
            else:
                return random_index - length_first_range
            
    def start_minute(self):
        return self.start
    
    def end_minute(self):
        return self.end



