import sys

def ec2_instance_info(value, return_key):
    # collect results from aws ec2 describe-instances result
    results = []
    for reservation in value['Reservations']:
      for instance in reservation['Instances']:
         results.append(instance[return_key])

    return results

def has_key(value, key):
    return value.has_key(key)

def list_of_dicts_to_list(value, first_key, second_key=None):
    # creates new list that will contain values of first_key if found, if not found then second_key
    results = []
    for mydict in value:
      if mydict.has_key(first_key):
          results.append(mydict[first_key])
      elif second_key and mydict.has_key(second_key):
          results.append(mydict[second_key])

    return results

def startswith(value, prefix):
    return value.startswith(prefix)

def debug_filter(value):
    # shows information about type and value. Useful for debugging strange issues with variables.
    sys.stdout.write('type name = ' + type(value).__name__ + '\n')
    sys.stdout.write('str = ' + str(value) + '\n')
    sys.stdout.write('repr = ' + repr(value) + '\n')
    return value

class FilterModule(object):
    ''' Ansible core jinja2 filters '''

    def filters(self):
        return {
            'ec2_instance_info': ec2_instance_info,
            'has_key': has_key,
            'list_of_dicts_to_list': list_of_dicts_to_list,
            'startswith': startswith,
            'debug_filter': debug_filter
        }
