import pandas as pd
from django.core.paginator import EmptyPage, Paginator
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Station
from .serializers import StationSerializer


class UploadFileView(APIView):
    @extend_schema(
        tags=["Станция"],
        summary="Загрузка файла со станциями",
        description=(
            "Позволяет загружать Excel-файл с данными базовых станций. "
            "\n\nФайл должен содержать столбцы: `ne`, `address`, `coordinates`, `technology`, `status`. "
            "Пример координат: `43.5,54.2`. Поддерживаемые технологии: `gsm`, `umts`, `lte`."
        ),
        request={
            "multipart/form-data": {
                "type": "object",
                "properties": {
                    "file": {
                        "type": "string",
                        "format": "binary",
                        "description": "Excel-файл с данными станций",
                    }
                },
            }
        },
        responses={
            201: {
                "type": "object",
                "properties": {"message": {"type": "string"}},
                "example": {"message": "Файл успешно загружен. Добавлено 10 записей."},
            },
            400: {
                "type": "object",
                "properties": {
                    "error": {"type": "string"},
                    "details": {"type": "array", "items": {"type": "string"}},
                },
                "example": {
                    "error": "Некоторые строки содержат ошибки.",
                    "details": ["Ошибка в строке 3: Некорректный формат координат"],
                },
            },
        },
    )
    def post(self, request):
        # Проверяем наличие файла
        file = request.FILES.get("file")
        if not file:
            return Response(
                {"error": "Файл не найден"}, status=status.HTTP_400_BAD_REQUEST
            )

        # Читаем Excel файл
        try:
            data = pd.read_excel(file)
        except ValueError as ve:
            return Response(
                {"error": f"Ошибка чтения файла: {str(ve)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        except Exception as e:
            return Response(
                {"error": f"Неверный формат файла: {str(e)}"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Проверяем обязательные столбцы
        required_columns = {"ne", "address", "coordinates", "technology", "status"}
        missing_columns = required_columns - set(data.columns)
        if missing_columns:
            return Response(
                {
                    "error": f'Отсутствуют обязательные столбцы: {", ".join(missing_columns)}'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Подготовка данных для сериализатора
        rows = []
        errors = []

        for index, row in data.iterrows():
            try:
                # Преобразуем координаты
                latitude, longitude = map(float, row["coordinates"].split(","))

                # Преобразуем технологии
                technologies = (
                    row["technology"].split(", ") if pd.notna(row["technology"]) else []
                )
                gsm = "gsm" in technologies
                umts = "umts" in technologies
                lte = "lte" in technologies

                # Добавляем данные для сериализатора
                rows.append(
                    {
                        "ne": row["ne"],
                        "address": row["address"],
                        "latitude": latitude,
                        "longitude": longitude,
                        "gsm": gsm,
                        "umts": umts,
                        "lte": lte,
                        "status": bool(row["status"]),
                    }
                )
            except Exception as e:
                errors.append(f"Ошибка в строке {index + 1}: {str(e)}")

        # Если есть ошибки преобразования, возвращаем их клиенту
        if errors:
            return Response(
                {"error": "Некоторые строки содержат ошибки.", "details": errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Проверяем данные через сериализатор
        serializer = StationSerializer(data=rows, many=True)
        if not serializer.is_valid():
            return Response(
                {"error": "Ошибка валидации данных.", "details": serializer.errors},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Сохраняем валидные данные
        serializer.save()
        return Response(
            {"message": f"Файл успешно загружен. Добавлено {len(rows)} записей."},
            status=status.HTTP_201_CREATED,
        )


@extend_schema(
    tags=["Станция"],
    summary="Список станций (JSON)",
    description="Возвращает список всех станций в формате JSON.",
)
class StationListAPIView(ListAPIView):
    queryset = Station.objects.all()
    serializer_class = StationSerializer


@extend_schema(
    tags=["Станция"],
    summary="HTML-страница с таблицей станций",
    description=(
        "Возвращает HTML-страницу с таблицей станций. "
        "Каждая строка содержит информацию о станции: ID, координаты, адрес, технологии и статус. "
        "Поддерживается пагинация через GET-параметр `page` (по умолчанию 5 записей на страницу)."
    ),
)
class StationHTMLView(APIView):
    def get(self, request):
        stations = Station.objects.all()
        page_number = request.GET.get("page", 1)
        paginator = Paginator(stations, 5)

        try:
            page = paginator.page(page_number)
        except EmptyPage:
            page = paginator.page(paginator.num_pages)

        return render(
            request, "stations.html", {"stations": page.object_list, "page": page}
        )
