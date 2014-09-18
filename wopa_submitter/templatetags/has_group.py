from django.contrib.auth.models import Group
from django import template
register = template.Library()

@register.filter(name='has_group')
def has_group(user, group_name):
	print "here" 
	group = Group.objects.get(name=group_name) 
	print group
	print user ,group_name
	return True if group in user.groups.all() else False
