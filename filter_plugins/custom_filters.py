import sys


def ec2_instance_info(value, return_key):
    # collect results from aws ec2 describe-instances result
    results = []
    for reservation in value['Reservations']:
        for instance in reservation['Instances']:
            results.append(instance[return_key])
    return results


def has_key(value, key):
    return key in value


def list_of_dicts_to_list(value, first_key, second_key=None):
    # creates new list that will contain values of first_key if found, if not found then second_key
    results = []
    for mydict in value:
        if first_key in mydict:
            results.append(mydict[first_key])
        elif second_key and second_key in mydict:
            results.append(mydict[second_key])
    return results


def add_file_attribute(value, template_key="template", name_key="name", file_key="file"):
    """ add file attribute to passed list of dictionaries """
    result = []
    for mydict in value:
        if template_key in mydict:
            mydict[file_key] = mydict[template_key]
        else:
            mydict[file_key] = mydict[name_key]
        result.append(mydict)
    return result


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
            'add_file_attribute': add_file_attribute,
            'startswith': startswith,
            'debug_filter': debug_filter
        }
