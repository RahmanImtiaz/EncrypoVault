from abc import ABC, abstractmethod

class AccountType(ABC):
    """Interface for different account types"""
    
    @abstractmethod
    def get_type_name(self):
        """Return the name of the account type"""
        pass
    
    @abstractmethod
    def get_transaction_limit(self):
        """Return the transaction limit for this account type"""
        pass

    @abstractmethod
    def uses_real_funds(self):
        """Returns whether this account type uses real cryptocurrency"""
        pass


class Advanced(AccountType):
    """Advanced account type with full features"""

    def switchToBeginner(self):
        return Beginner()
    
    def get_type_name(self):
        return "Advanced"
    
    def get_transaction_limit(self):
        return float('inf')  # Unlimited transactions
    
    def uses_real_funds(self):
        return True
    


class Beginner(AccountType):
    """Beginner account type with limited features"""
    
    def get_type_name(self):
        return "Beginner"
    
    def get_transaction_limit(self):
        return 1000.0  # Limited to $1000 per day
    
    def showTutorials(self):
        pass

    def switchToAdvanced(self):
        return Advanced()
    
    def uses_real_funds(self):
        return True

class Tester(AccountType):
    """Tester account type for testing purposes"""
    
    def get_type_name(self):
        return "Tester"
    
    def get_transaction_limit(self):
        return 100.0  # Very limited for testing
    
    def uses_real_funds(self):
        return False

    