import QuanTest1

class Task3:
    def __init__(self, number_of_bits, main_instance):
        self.number_of_bits = number_of_bits
        self.data = None
        self.min = None
        self.max = None
        self.number_of_levels = None
        self.delta = None
        self.number_range = []
        self.main = main_instance

    def get_min(self, var):
        if not var:  # Check if data is empty
            return None
        minimum = var[0]  # Initialize min with the first element
        for i in var:
            if i < minimum:
                minimum = i
        return minimum

    def get_max(self, var):
        if not var:  # Check if data is empty
            return None
        maximum = var[0]  # Initialize max with the first element
        for i in var:
            if i > maximum:  # Corrected comparison for max
                maximum = i
        return maximum

    def cal_delta(self):
        if self.number_of_levels > 0:  # Ensure we don't divide by zero
            return (self.max - self.min) / self.number_of_levels
        return None  # Return None if number_of_levels is not set or invalid

    def make_ranges(self):
        mn = self.min

        for i in range(self.number_of_levels):
            # Round mn and mn + step to 2 decimal places
            rounded_mn = round(mn, 2)  # Round to 2 decimal places
            rounded_high = round(mn + self.delta, 2)  # Round the upper limit to 2 decimal places
            self.number_range.append((rounded_mn, rounded_high))
            mn += self.delta

    def convert_data(self, data):
        print(self.delta)
        print(self.number_range)
        for i, (low, high) in enumerate(self.number_range):
            if low <= data <= high:
                return round((low+high)/2,2), i  # Map boundary values to the lower end
        return None, None  # Return None if no range is found

    def prepare_data(self, data):
        c = []
        b = []

        for i in data:
            converted_data, index = self.convert_data(i)
            c.append(converted_data)
            b.append(index)
        return c, b

    def convert_to_binary(self, value):
        if value is None:
            return '0' * self.number_of_bits  # Return a binary representation of zero if value is None
        m = ''
        while value > 0:
            m = str(value % 2) + m
            value //= 2
        while len(m) < self.number_of_bits:
            m = '0' + m
        return m
    #def cal_error(self):


    def run(self):
        self.data = self.main.read_file('Quan1_input.txt')

        self.min = self.get_min(self.data['data'])
        self.max = self.get_max(self.data['data'])

        self.number_of_levels = 2 ** self.number_of_bits
        self.delta = self.cal_delta()

        # Check if delta is calculated properly
        if self.delta is None:
            print("Error: Delta could not be calculated. Check min, max, and number_of_levels.")
            return  # Exit if delta is not valid

        self.make_ranges()

        updated_data = []
        updated_index = []
        updated_index_binary = []

        for x in self.data['data']:
            l, m = self.convert_data(x)
            if l is None or m is None:
                print(f"Warning: No range found for value {x}")
                continue  # Skip to the next value if no valid range is found
            updated_data.append(l)
            updated_index.append(m)

        for ind in updated_index:
            j = self.convert_to_binary(ind)
            updated_index_binary.append(j)

        self.main.create_file_array_input('amolal', updated_data, updated_index_binary)
        QuanTest1.QuantizationTest1('amolal.txt', updated_index_binary, updated_data)
