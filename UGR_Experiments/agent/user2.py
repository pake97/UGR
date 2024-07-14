import numpy as np

class User:
    def __init__(self, user_type):
        self.actions = []
        self.user_type = user_type
        self.policy = []
        self.actions=[]
        self.best_repair=None

    def set_actions(self, actions):
        self.actions = actions
    
    def set_policy(self, policy):
        self.policy = policy

    def set_best_repair(self, best_repair):
        self.best_repair = best_repair

    def get_type(self):
        return self.user_type
    
    def remove_action(self, action):
        
        if(action == self.best_repair):
            self.best_repair=""
        else:
            index = self.actions.index(action)
            self.actions.pop(index)
        

    def select_action_by_policy(self, answer_distribution,seed2):
        if(answer_distribution[0]==0):
            answer_idx= np.random.choice(len(self.actions))
            return self.actions[answer_idx]
        if(answer_distribution[0]==1):
            if(self.best_repair==""):
                answer_idx= np.random.choice(len(self.actions))
                return self.actions[answer_idx]
            else:
                return self.best_repair
        if(not self.best_repair==""):
            number_of_actions = len(self.actions)
            policy =[answer_distribution[0]]
            for i in range(number_of_actions):
                policy.append((1-answer_distribution[0])/(number_of_actions))
            selected_action_index = np.random.choice(number_of_actions+1,p =policy)

            if(selected_action_index==0):
                return self.best_repair
            else:    
                return self.actions[selected_action_index-1]
        else:
            number_of_actions = len(self.actions)
            policy =[]
            for i in range(number_of_actions):
                policy.append(1/(number_of_actions))
            selected_action_index = np.random.choice(number_of_actions,p =policy)
            return self.actions[selected_action_index]
        
            

    def select_action(self):
        sum_policy = sum(self.policy)
        if(sum_policy!=1):
            max = np.argmax(self.policy)
            self.policy[max]+=1-sum_policy
        selected_action_index = np.random.choice(len(self.actions)+1, p=self.policy)
        return self.actions[selected_action_index]

# Example Usage
if __name__ == "__main__":
    actions = ['action1', 'action2', 'action3']
    policy = [1,0,0]
    # Create an Oracle user
    oracle_user = User(user_type='Oracle')
    oracle_user.set_actions(actions)
    oracle_user.set_policy(policy)

    # Select actions for each user
    for _ in range(5):
        oracle_action = oracle_user.select_action()
        print(f"Oracle User Action: {oracle_action}")
