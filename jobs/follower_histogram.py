from mrjob.job import MRJob

class FollowerHistogram(MRJob):
    """
    A Map/Reduce job to count the number of followers each user has
    and then create a count of how many users have how many followers.
    
    Input::
    
        <user_id>\t<follower_id>
    
    Output::
    
        <num_followers>\t<num_users_who_have_that_mahy_followers>
    
    For example, for the following input data::
    
        1\t2
        1\t3
        1\t3
        2\t1
        3\t1
        3\t2
        3\t3
    
    The following would be output::
    
        2\t2
        3\t1
    
    That is to say that for this data set, there are 2 users who have 2
    followers and 1 user that has 3 followers.
    """
    # Map Step 1: Read the file in <user_id>\t<follower_id> and increment
    # the follower count for that <user_id>.
    def increment_followers(self, key, line):
        yield int(line.split('\t')[0]), 1

    # Reduce Step 1: Sum the number of followers for each <user_id>
    def sum_followers(self, id, followers):
        x = 0
        for f in followers:
            x += f
        yield id, x

    # Map Step 2: Increment the number of users who have the given number
    # of followers.
    def increment_users_per_follow_count(self, id, followers):
        yield followers, 1

    # Reduce Step 2: Sum the follower count for each number of followers
    def sum_users_per_follow_count(self, follow_count, users_count):
        x = 0
        for c in users_count:
            x += c
        yield follow_count, x

    def steps(self):
        return [self.mr(self.increment_followers, self.sum_followers),
                self.mr(self.increment_users_per_follow_count, 
                self.sum_users_per_follow_count)]

if __name__ == '__main__':
    FollowerHistogram.run()
