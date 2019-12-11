from django.shortcuts import render
from django.template.context_processors import csrf

from puppies.models import Puppy


def index(request):
    """

    :param request:
    :return:
    """
    args = {}
    args.update(csrf(request))
    args['puppy'] = Puppy.objects.all()

    # messages = ["This is message1", "This is message2"]
    # args = {'messages': messages}

    return render(request, 'index.html', args)
