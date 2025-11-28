# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Task
from .serializers import TaskSerializer

class TaskListCreateView(APIView):
    # GET: listar tareas
    def get(self, request):
        tasks = Task.objects.all()
        serializer = TaskSerializer(tasks, many=True)
        return Response(serializer.data)

    # POST: crear tarea
    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TaskDetailView(APIView):
    # método auxiliar
    def get_object(self, pk):
        try:
            return Task.objects.get(pk=pk)
        except Task.DoesNotExist:
            return None

    # GET /tasks/{id}
    def get(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response({"error": "Task not found"}, status=404)
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    # PUT /tasks/{id}
    def put(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response({"error": "Task not found"}, status=404)

        serializer = TaskSerializer(task, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=400)

    # DELETE /tasks/{id}
    def delete(self, request, pk):
        task = self.get_object(pk)
        if task is None:
            return Response({"error": "Task not found"}, status=404)

        task.delete()
        return Response(status=204)