
def ec2_instance_info(value, return_key):
    # collect results from aws ec2 describe-instances result
    results = []
    for reservation in value['Reservations']:
      for instance in reservation['Instances']:
         results.append(instance[return_key])

    return results

class FilterModule(object):
    ''' Ansible core jinja2 filters '''

    def filters(self):
        return {
            'ec2_instance_info': ec2_instance_info,
        }
