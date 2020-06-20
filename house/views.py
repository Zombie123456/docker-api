import os
import xlrd
from collections import OrderedDict

from django.views.decorators.csrf import csrf_exempt
from django.db import transaction
from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_condition import Or
from rest_framework.decorators import renderer_classes, api_view, permission_classes

from house.models import House, BuildNum
from house.serializers import HouseManagerSerializer, HouseStaffSerializer, BuildNumSerializer
from house.filters import StaffFilter
from loginsvc.permissions import IsSeller, IsManager, IsStaff, ReadOnly
from demo.utils import CampaignRenderer
from demo.lib import constans
from loginsvc.views import generate_response


class HouseBaseViewSet(viewsets.GenericViewSet,
                       mixins.UpdateModelMixin,
                       mixins.RetrieveModelMixin,
                       mixins.CreateModelMixin,):

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


class HouseViewSet(mixins.DestroyModelMixin, HouseBaseViewSet):
    model = House
    queryset = House.objects.all().order_by('floor')
    serializer_class = HouseManagerSerializer
    permission_classes = [Or(IsManager, IsStaff)]
    filter_class = StaffFilter
    renderer_classes = [CampaignRenderer]


class HouseStaffViewSet(HouseBaseViewSet):

    model = House
    queryset = House.objects.filter(status=House.CAN_SELA)
    serializer_class = HouseStaffSerializer
    permission_classes = [Or(IsSeller, IsManager, IsStaff)]
    filter_class = StaffFilter
    renderer_classes = [CampaignRenderer]

    def get_queryset(self):
        if self.request.GET.get('my_sale_house'):
            return House.objects.filter(sela_staff=self.request.user.staff_user)
        return self.queryset


class BuildNumViewSet(viewsets.ModelViewSet):
    model = BuildNum
    queryset = BuildNum.objects.all()
    permission_classes = [Or(IsStaff, IsManager, ReadOnly)]
    serializer_class = BuildNumSerializer


@api_view(['POST'])
@renderer_classes([CampaignRenderer])
@csrf_exempt
@permission_classes([IsManager])
def import_excel_file(request):
    import_file = request.FILES.get('import_file')

    if not import_file:
        return generate_response(constans.NOT_OK, msg='No incoming files')

    file_name = import_file.__str__()
    file_format = os.path.splitext(file_name)[-1]

    if '.xlsx' in file_format:
        workbook = xlrd.open_workbook(file_contents=import_file.read())
        worksheet = workbook.sheet_by_index(0)
        try:
            with transaction.atomic():
                row = '1-2'
                build_obj = BuildNum.objects.create(name=worksheet.row_values(0)[0], code=worksheet.row_values(0)[0])
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
                        'build_num': build_obj
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
        return generate_response(constans.NOT_OK, msg='No incoming files')

    file_name = import_file.__str__()
    file_format = os.path.splitext(file_name)[-1]

    if '.xlsx' in file_format:
        workbook = xlrd.open_workbook(file_contents=import_file.read())
        worksheet = workbook.sheet_by_index(0)
        try:
            with transaction.atomic():
                row = '1-2'
                obj_list = []
                for i in range(2, worksheet.nrows):
                    data = worksheet.row_values(i)
                    if data[1].strip() == '子母':
                        pass
                    db_data = {
                        'floor': int(data[0][:2]),
                        'set_num_1': data[0]
                    }

        except Exception as e:
            return generate_response(constans.NOT_OK, msg=f'发生错误，请检查第{row}行的数据: {e}')

        return generate_response(constans.ALL_OK, msg='导入成功')
    return generate_response(constans.NOT_OK, msg=f'只支持 xlsx 文件')
