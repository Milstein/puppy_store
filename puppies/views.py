from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.template.context_processors import csrf
from django.utils import timezone
from django.views import generic
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from puppies.forms import PuppyForm
from puppies.models import Puppy
from puppies.serializers import PuppySerializer


class IndexView(generic.ListView):
    # the ListView generic view uses a default template called <app name>/<model name>_list.html i.e.
    # polls/question_list.html if not set 'template_name'
    # template_name = 'polls/index.html'

    # The automatically generated context variable is 'question_list' if not set this variable 'context_object_name'
    # context_object_name = 'latest_questions'

    def get_queryset(self):
        """
            Return the last five published questions (not including those set to be
            published in the future).
            """
        return Puppy.objects.filter(
            pub_date__lte=timezone.now()
        ).order_by('-pub_date')[:5]
        # return Question.objects.order_by('-pub_date')[:5]


def index(request):
    """

    :param request:
    :return:
    """
    args = {}
    args.update(csrf(request))
    args['puppy'] = Puppy.objects.all()
    # args['puppy'] = Puppy.objects.order_by('-created_at')[:5]

    # messages = ["This is message1", "This is message2"]
    # args = {'messages': messages}

    return render(request, 'puppies/index.html', args)

    # def get(self, request):
    #     contact_form = ContactForm()
    #     return render(request, 'rsna/contact.html', {
    #         'form': contact_form
    #     })


def add(request):
    if request.POST:
        form = PuppyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/')
    else:
        form = PuppyForm()

    args = {}
    args.update(csrf(request))
    args['form'] = form
    return render(request, 'puppies/add.html', args)


@api_view(['GET', 'DELETE', 'PUT'])
def get_delete_update_puppy(request, pk):
    """

    :param request:
    :param pk:
    :return:
    """
    try:
        puppy = Puppy.objects.get(pk=pk)
    except Puppy.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    # get details of a single puppy
    if request.method == 'GET':
        # return Response({})
        serializer = PuppySerializer(puppy)
        return Response(serializer.data)
    # delete a single puppy
    elif request.method == 'DELETE':
        # return Response({})
        puppy.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
    # update details of a single puppy
    elif request.method == 'PUT':
        # return Response({})
        serializer = PuppySerializer(puppy, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET', 'POST'])
def get_post_puppies(request):
    """

    :param request:
    :return:
    """
    # get all puppies
    if request.method == 'GET':
        # return Response({})
        puppies = Puppy.objects.all()
        serializer = PuppySerializer(puppies, many=True)
        return Response(serializer.data)
    # insert a new record for a puppy
    elif request.method == 'POST':
        # return Response({})
        data = {
            'name': request.data.get('name'),
            'age': int(request.data.get('age')),
            'breed': request.data.get('breed'),
            'color': request.data.get('color')
        }
        serializer = PuppySerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
