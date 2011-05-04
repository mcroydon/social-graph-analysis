from mrjob.job import MRJob

class FollowerCount(MRJob):
    """
    A simple single step Map/Reduce job to count the number of followers
    each user has.
    
    Input::
    
        <user_id>\t<follower_id>
    
    Output::
    
        <user_id>\t<num_followers>
    
    For example, for the following input data::
    
        1\t2
        1\t3
        1\t3
        2\t1
        3\t1
        3\t2
        3\t3
    
    The following would be output::
    
        1\t3
        2\t1
        3\t3
    """
    # Read the file in <user_id>\t<follower_id> and increment the follower 
    # count for that <user_id>.
    def mapper(self, key, line):
        yield int(line.split('\t')[0]), 1

    # Reduce Step 1: Sum the number of followers for each <user_id>
    def reducer(self, id, followers):
        yield id, sum(followers)

if __name__ == '__main__':
    FollowerCount.run()
