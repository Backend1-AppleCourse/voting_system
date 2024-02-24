# voter - no duplicates -> 
# vote - no duplicates & immutable-> dictionary/set
# candidate - immutable

# each voter can only have one vote
# candidate can have multiple positions
# 

# imports
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import hashlib
import random

candidates = [
    {'name': 'John Doe', 'positions': ['President', 'Vice President']},
    {'name': 'Jane Doe', 'positions': ['Secretary', 'Treasurer']},
    {'name': 'John Smith', 'positions': ['Secretary', 'President']}
]

voters = [
    {'name': 'name1, age: 21', 'addr': "address 1"},
    {'name': 'name2, age: 22', 'addr': "address 2"},
    {'name': 'name3, age: 23', 'addr': "address 3"},
    {'name': 'name4, age: 24', 'addr': "address 4"},
    {'name': 'name5, age: 25', 'addr': "address 5"},
    {'name': 'name6, age: 26', 'addr': "address 6"},
    {'name': 'name7, age: 27', 'addr': "address 7"},
    {'name': 'name8, age: 28', 'addr': "address 8"},
    {'name': 'name9, age: 29', 'addr': "address 9"},
    {'name': 'name10, age: 30', 'addr': "address 10"}
]

# DB of the system
class DB:
    def __init__(self):
        self.candidates = set()
        self.voters = set()
        self.votes = set()
        self.__passcphrase = "my_secret_passphrase"
        self.__key = hashlib.sha256(self.__passcphrase.encode()).digest()
    
    def __str__(self):
        return f'Voters: {len(self.voters)} Candidates: {len(self.candidates)} Votes: {len(self.votes)}'
    
    def addVoter(self, voter):
        if not isinstance(voter, Voter):
            raise ValueError('Voter is required')
        # validating if voter already exists
        for v in self.voters:
            if v.name == voter.name and v.age == voter.age and v.addr == voter.addr: 
                raise ValueError('Voter already exists')
        self.voters.add(voter)

    def __create_user_key(name, age, address, key):
        data = f"{name}|{age}|{address}"
        data_bytes = pad(data.encode(), AES.block_size) 
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted_data = cipher.encrypt(data_bytes)
        return encrypted_data
    
    def addVote(self, voter, candidate):
        id = self.__create_user_key(voter.name, voter.age, voter.addr, self.__key)
        self.votes.add({id, candidate})

    def voted(self, voter):
        id = self.__create_user_key(voter.name, voter.age, voter.addr, self.__key)
        for vote in self.votes:
            if vote[0] == id:
                return True
    
    def getVoters(self):
        return self.voters
    
    def getVotes(self):
        return self.votes

    def addCandidate(self, candidate):
        if not isinstance(candidate, Candidate):
            raise ValueError('Candidate is required')
        self.candidates.add(candidate)

    def addPositionToCandidate(self, candidate, position):
        if not isinstance(candidate, Candidate):
            raise ValueError('Candidate is required')
        if not isinstance(position, str):
            raise ValueError('Position is required as string')
        for c in self.candidates:
            if c.name == candidate.name:
                c.addPosition(position)

    def importCandidates(self, candidates_list):
        for candidate in candidates_list:
            self.addCandidate(Candidate(candidate.name, candidate.positions))
    def importVoters(self, voter_list):
        for voter in voter_list:
            self.addVoter(Voter(voter.name, voter.age, voter.addr))

# voter class
class Voter:
    def __init__(self,name, age, addr):
        if not name:
            raise ValueError('Name is required')
        if not age or not age.isdigit():
            raise ValueError('Age is required and must be a number')
        if not addr:
            raise ValueError('Address is required')

        self.name = name
        self.age = age
        self.addr = addr
    
    def __str__(self):
        return f'{self.name} {self.age} {self.addr}'

    def vote(self):
        return {Vote(self, candidate)}

class Candidate:
    def __init__(self, name):
        if not name:
            raise ValueError('Name is required')
        self.name = name
        self.positions = set()
    
    def __str__(self):
        return f'{self.name} {self.positions}'

    def addPosition(self, position):
        if not isinstance(position, str):
            raise ValueError('Position is required as string')
        self.positions.add(position)
    
    def addPositions(self, positions):
        if not isinstance(positions, list):
            raise ValueError('Positions is required as list')
        for position in positions:
            self.addPosition(position)


db = DB()

print(db)