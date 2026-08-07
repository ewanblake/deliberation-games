class BurdenManager:

    def __init__(self):

        # No burden exists at the start point of a dialogue
        self.current_burden = None

        # Will store all burdens created during the dialogue
        self.history = []

    def create_burden(self, owner, proposal):

        # Do not create another burden if one is already active!
        if self.current_burden is not None:

            return False

        self.current_burden = {
            "owner": owner,
            "proposal": proposal,
            "status": "CREATED"
        }

        self.history.append({
            "owner": owner,
            "proposal": proposal,
            "status": "CREATED"
        })

        return True

    def activate_burden(self):

        if self.current_burden is None:
            return False

        if self.current_burden["status"] != "CREATED":
            return False

        self.current_burden["status"] = "ACTIVE"

        self.history.append({
            "owner": self.current_burden["owner"],
            "proposal": self.current_burden["proposal"],
            "status": "ACTIVE"
        })

        return True

    def satisfy_burden(self):

        if self.current_burden is None:
            return False

        if self.current_burden["status"] != "ACTIVE":
            return False

        self.current_burden["status"] = "SATISFIED"

        self.history.append({
            "owner": self.current_burden["owner"],
            "proposal": self.curent_burden["proposal"],
            "status": "SATISFIED"
        })

        return True

    def resolve_burden(self):

        if self.current_burden is None:
            return False

        self.current_burden["status"] = "RESOLVED"

        self.history.append({
            "owner": self.current_burden["owner"],
            "proposal": self.current_burden["proposal"],
            "status": "RESOLVED"
        })

        self.current_burden = None

        return True

    def remove_burden(self):

        return self.resolve_burden()

    def is_active(self):

        return (
            self.current_burden is not None
            and 
            self.current_burden["status"] == "ACTIVE"
        )

    def is_created(self):

        return (
            self.current_burden is not None
            and
            self.current_burden["status"] == "CREATED"
        )

    def is_satisfied(self):

        return (
            self.current_burden is not None
            and
            self.current_burden["status"] == "SATISFIED"
        )

    def has_burden(self):

        return self.current_burden is not None

    def get_status(self):

        if self.current_burden:

            return self.current_burden["status"]
        
        return None
    
    def get_owner(self):

        if self.current_burden:

            return self.current_burden["owner"]
        
        return None
    
    def get_proposal(self):

        if self.current_burden:

            return self.current_burden["proposal"]
        
        return None
    
    def to_dict(self):

        if not self.current_burden:

            return {
                "burden_status": None,
                "burden_owner": None,
                "burden_proposal": None
            }
        
        return {
            "burden_status": self.current_burden["status"],
            "burden_owner": self.current_burden["owner"],
            "burden_proposal": self.current_burden["proposal"]
        }

    def get_history(self):

        return self.history