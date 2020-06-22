import os
import xlrd
from collections import OrderedDict

from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_condition import Or
from rest_framework.decorators import renderer_classes, api_view, permission_classes

from house.models import House, BuildNum, Community, ImportLog
from house.serializers import HouseManagerSerializer, BuildNumSerializer, CommunitySerializer, \
    HouseManagerGetSerializer, ImportLogSerializer
from house.filters import StaffFilter, BuildNumFilter
from loginsvc.permissions import IsSeller, IsManager, IsStaff
from demo.utils import CampaignRenderer
from demo.lib import constans
from loginsvc.views import generate_response


class HouseBaseViewSet(viewsets.GenericViewSet,
                       mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin):

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        ret = OrderedDict()
        for i in serializer.data:
            if ret.get(i['floor']):
                ret[i['floor']].append(i)
            else:
                ret[i['floor']] = [i]

        return Response(ret)


class HouseViewSet(mixins.DestroyModelMixin,
                   HouseBaseViewSet,
                   mixins.CreateModelMixin):
    model = House
    queryset = House.objects.all().order_by('floor')
    permission_classes = [Or(IsManager, IsStaff, IsSeller)]
    filter_class = StaffFilter
    renderer_classes = [CampaignRenderer]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            try:
                self.get_object()
            except:
                return HouseManagerGetSerializer

        return HouseManagerSerializer


class BuildNumViewSet(viewsets.ModelViewSet):
    model = BuildNum
    queryset = BuildNum.objects.all()
    permission_classes = [Or(IsStaff, IsManager, IsSeller)]
    serializer_class = BuildNumSerializer
    filter_class = BuildNumFilter


class CommunityViewSet(viewsets.ModelViewSet):
    model = Community
    queryset = Community.objects.all()
    permission_classes = [Or(IsManager, IsStaff, IsSeller)]
    renderer_classes = [CampaignRenderer]
    serializer_class = CommunitySerializer


class ImportLogViewSet(viewsets.GenericViewSet,
                       mixins.DestroyModelMixin,
                       mixins.ListModelMixin):
    model = ImportLog
    queryset = ImportLog.objects.all()
    permission_classes = [IsManager]
    renderer_classes = [CampaignRenderer]
    serializer_class = ImportLogSerializer


@api_view(['POST'])
@renderer_classes([CampaignRenderer])
@csrf_exempt
@permission_classes([IsManager])
def import_excel_file(request):
    import_file = request.FILES.get('import_file')

    if not import_file:
        return generate_response(constans.NOT_OK, msg='请上传文件')

    try:
        build = BuildNum.objects.get(id=request.POST.get('build_id'))
    except:
        return generate_response(constans.NOT_OK, msg='请选择哪一栋楼')

    file_name = import_file.__str__()
    file_format = os.path.splitext(file_name)[-1]

    if '.xlsx' in file_format:
        workbook = xlrd.open_workbook(file_contents=import_file.read())
        worksheet = workbook.sheet_by_index(0)
        try:
            with transaction.atomic():
                import_log = ImportLog.objects.create(file_name=file_name)
                row = '1-2'
                obj_list = []
                for i in range(2, worksheet.nrows):
                    row = i
                    try:
                        floor = int(worksheet.row_values(i)[0])
                    except:
                        floor = worksheet.row_values(i)[0]
                    data = {
                        'floor': floor,
                        'room_num': worksheet.row_values(i)[1].strip(),
                        'unit_type': worksheet.row_values(i)[2].strip(),
                        'area': worksheet.row_values(i)[3],
                        'unit_price': worksheet.row_values(i)[4],
                        'price': worksheet.row_values(i)[5],
                        'build_num': build,
                        'import_log': import_log
                    }
                    obj_list.append(House(**data))
                House.objects.bulk_create(obj_list)
        except Exception as e:
            return generate_response(constans.NOT_OK, msg=f'发生错误，请检查第{row}行的数据: {e}')

        return generate_response(constans.ALL_OK, msg='导入成功')
    return generate_response(constans.NOT_OK, msg=f'只支持 xlsx 文件')


@api_view(['POST'])
@renderer_classes([CampaignRenderer])
@csrf_exempt
@permission_classes([IsManager])
def import_car_excel_file(request):
    import_file = request.FILES.get('import_file')

    if not import_file:
        return generate_response(constans.NOT_OK, msg='请上传文件')
    try:
        build = BuildNum.objects.get(id=request.POST.get('build_id'))
    except:
        return generate_response(constans.NOT_OK, msg='请选择哪一栋楼')

    file_name = import_file.__str__()
    file_format = os.path.splitext(file_name)[-1]

    if '.xlsx' in file_format:
        workbook = xlrd.open_workbook(file_contents=import_file.read())
        worksheet = workbook.sheet_by_index(0)
        try:
            with transaction.atomic():
                import_log = ImportLog.objects.create(file_name=file_name)
                row = '1-2'
                obj_list = []
                for i in range(2, worksheet.nrows):
                    row = i
                    data = worksheet.row_values(i)
                    if not data[2]:
                        continue
                    if data[1].strip() == '子母':
                        set_type = House.MOTHER
                    else:
                        set_type = House.NORMAL

                    db_data = {
                        'floor': int(data[0][:2]),
                        'room_num': data[0],
                        'price': data[3],
                        'set_type': set_type,
                        'build_num': build,
                        'is_car': True,
                        'import_log': import_log
                    }
                    obj_list.append(House(**db_data))

                House.objects.bulk_create(obj_list)

        except Exception as e:
            return generate_response(constans.NOT_OK, msg=f'发生错误，请检查第{row}行的数据: {e}')

        return generate_response(constans.ALL_OK, msg='导入成功')
    return generate_response(constans.NOT_OK, msg=f'只支持 xlsx 文件')
