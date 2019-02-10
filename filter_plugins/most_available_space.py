#!/usr/bin/python
class FilterModule(object):
    def filters(self):
        return {
            'sortbysubkey': self.sortbysubkey,
        }

    def sortbysubkey(self, dict_to_sort, sorting_key):
        sorted_dict = sorted(dict_to_sort.items(),
                             key=lambda x: x[1][sorting_key], reverse=True)
        # Return with the key name of our highest value
        return sorted_dict[0][0]
