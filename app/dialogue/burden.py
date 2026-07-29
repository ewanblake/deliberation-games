class BurdenManager:

    def __init__(self):

        # No burden exists at the start point of a dialogue
        self.current_burden = None

    def create_burden(self, owner, proposal):

        self.current_burden = {
            "owner": owner, 
            "proposal": proposal,
            "status": "INACTIVE"
        }

    def activate_burden(self):

        if self.current_burden:

            self.current_burden["status"] = "ACTIVE"

    def satisfy_burden(self):

        if self.current_burden:

            self.current_burden["status"] = "SATISFIED"

    def remove_burden(self):

        self.current_burden = None

    def is_active(self):

        return (
            self.current_burden is not None
            and self.current_burden["status"] == "ACTIVE"
        )

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
            "burden_status": self.get_status(),
            "burden_owner": self.get_owner(),
            "burden_proposal": self.get_proposal()
        }