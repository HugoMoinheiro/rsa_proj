class Vehicle:
    def __init__(self, row, exit, id):
        self.row=row
        self.exit=exit
        self.id=id

    def vehicle_info(self):
        return f' Vehicle: {self.id}' + " / Row: " + f'{self.row}' + " / Exit: " + f'{self.exit}'
        
    def process_initial_cause_code(self):
        if self.row == 1:
            if self.exit == 1:
                return 1
            elif self.exit == 2:
                return 2
            else:
                return 3
        elif self.row == 2:
            if self.exit == 1:
                return 4
            elif self.exit == 2:
                return 5
            else:
                return 6
        else:
            if self.exit == 1:
                return 7
            elif self.exit == 2:
                return 8
            else:
                return 9