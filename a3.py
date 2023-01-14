class PointDatabase:
    def __init__(self,pointlist):
        self.abcissa = sorted(pointlist)
        self.sorted_levels = []
        self.sorted_levels.append(self.abcissa.copy())
        
        # abcissa contains the points of pointlist sorted by x then y
        # sorted_levels contains logn lists such that sorted_levels[i] is a list whose subarrays of length 2^i of abcissa are sorted by y
        # where these subarrays are mutually disjoint
        # since every list of sorted_levels is of length n
        # Time complexity of constructor = O(nlogn)
        n = len(pointlist)
        level = 1
        jump = 1
        while pow(2,level-1)<=n:
            l = []
            i = 0
            j = jump + i
            while i<n and j<n:
                limi = min(n,i+jump)
                limj = min(n,j+jump)
                while i<limi and j<limj:
                    if self.sorted_levels[level-1][i][1]<=self.sorted_levels[level-1][j][1]:
                        l.append(self.sorted_levels[level-1][i])
                        i+=1
                    else:
                        l.append(self.sorted_levels[level-1][j])
                        j+=1
                if i<limi:
                    while i<limi:
                        l.append(self.sorted_levels[level-1][i])
                        i+=1
                if j<limj:
                    while j<limj:
                        l.append(self.sorted_levels[level-1][j])
                        j+=1

                i += jump
                j += jump

            if i<n:
                while i<n:
                    l.append(self.sorted_levels[level-1][i])
                    i+=1

            self.sorted_levels.append(l)
            jump*=2
            level+=1
            
    def searchNearby(self,point,d):
        x,y = point
        leftx = x-d # lower limit of the abcissa
        rightx = x+d # upper limit of the abcissa
        upy = y+d # upper limit of ordinate
        downy = y-d # lower limit of ordinate
        
        i = 0
        j = len(self.abcissa)
        left_index = 0 
        # Using binary search to find the first point whose abcissa is >= the lower limit
        while i<j:
            mid = (i+j)//2
            if self.abcissa[mid][0]<leftx:
                i = mid+1
                left_index = mid+1
            else:
                left_index = mid
                j = mid

        i = 0
        j = len(self.abcissa)
        right_index = len(self.abcissa)
        # using binary search to find the last point whose abcissa is <= the upper limit
        while i<j:
            mid = (i+j)//2
            if self.abcissa[mid][0]<=rightx:
                i = mid+1
            else:
                right_index = mid
                j = mid

        output = []
        if left_index==right_index: return output

        l = left_index

        # For the entire search range of length d there are O(logd) regions 
        # The regions are of the form d/2,d/4....
        # Time complexity = m + logd -1 + logd - 2 +.... 1 = O(m + (logd)^2) = O(m + (logn)^2) where search range is n in worst case
        # and m is the no of valid points added in the output list
        while l<right_index: 
            # finding the largest list of len 2^k starting from l where k = 0,1,2,....
            level = 0
            w = l
            while w>=2 and w%2==0:
                level+=1
                w/=2

            # r denotes the end point of the above array
            # halving the size of the array till r does not exceed right_index
            r = l+pow(2,level)
            while r>right_index:
                r = l + (r-l)//2
                level -= 1

            i,j = l,r
            lower,upper = l,r
            
            # Using binary search in the given subarray to find the first point whose ordinate is >= the lower limit
            while i<j:
                mid = (i+j)//2
                if self.sorted_levels[level][mid][1]<downy:
                    i = mid+1
                    lower = mid+1
                else:
                    lower = mid
                    j = mid

            i,j = l,r
            # Using binary search in the given subarray to find the last point whose ordinate is <= the upper limit
            while i<j:
                mid = (i+j)//2
                if self.sorted_levels[level][mid][1]<=upy:
                    i = mid+1
                    upper = mid+1
                else:
                    upper = mid
                    j = mid

            # The points between these limits satisfy both the conditions for the range of x,y
            l = r
            # Append the valid points in the output list
            for i in range(lower,upper):
                output.append(self.sorted_levels[level][i])
        return output