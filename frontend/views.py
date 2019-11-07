from django.shortcuts import render
from django.http import HttpResponse
from django.shortcuts import render,redirect,HttpResponse
from frontend import  models
import numpy as np
# Create your views here.

def questions(request):
    global weight
    global functions
    global performance
    global expense
    global other_demands
    if request.method == 'POST':
        functions = request.POST.getlist('functions[]')
        performance = request.POST.getlist('performance[]')
        weight = request.POST.get('weight')
        expense = request.POST.get('expense')
        other_demands = request.POST.getlist('other_demands[]')
        print(functions,performance,weight,expense,other_demands)
    return render(request,'mainpart/questions.html')


def recommend(request):

    #首先根据花费设定预算阈值
    scores_type = []
    price_threshold = 0
    if expense == "economic":
        price_threshold = 7000
    elif expense == "average":
        price_threshold = 12000
    if expense == "much":
        price_threshold = 24000

    #其次根据笔记本电脑负重设定重量阈值
    global weight
    weight_threshold = 0
    if weight == "cannot":
        weight_threshold = 3.0
    if weight == "possible":
        weight_threshold = 3.5
    if weight == "okey":
        weight_threshold = 4.0

    #对笔记本性能要求的计算
    performance_weight = [0,0,0,0,0,0]
    performance_describe = ['no demand','screen','big_size','battery','disk','strong performance']
    performance_describe_score = ['none','screen_score','size_score','battery_score','disk_score','processor_score']
    for des in performance:
        idx = performance_describe.index(des)
        performance_weight[idx] = 1
        if idx!= 0:
            scores_type.append(performance_describe_score[idx])

    pc_score = []
    pcs = models.computer.objects.filter(price__lt=price_threshold,weight__lt=weight_threshold)
    #pcs = models.computer.objects.filter(price__lt=price_threshold)
    for pc in pcs:
        score = []
        score.append(0)
        score.append(pc.screen_score)
        score.append(pc.size_score)
        score.append(pc.battery_score)
        score.append(pc.disk_score)
        score.append(pc.processor_score)
        weight = np.array(performance_weight)
        score = np.array(score)
        performance_score = np.sum(np.multiply(weight,score))
        dic = {"id":pc.id,"name":pc.name,"score":performance_score}
        pc_score.append(dic)

    #计算其他需求的得分
    if "beautiful" in other_demands:
        scores_type.append("beauty_score")
        for pc in pc_score:
            id = pc["id"]
            pc_info = models.computer.objects.get(id=id)
            pc["score"] = pc["score"] + pc_info.beauty_score

    if "new types" in other_demands:
        scores_type.append("newtype_score")
        for pc in pc_score:
            id = pc["id"]
            pc_info = models.computer.objects.get(id=id)
            if pc_info.year == 2019:
                pc["score"] = pc["score"] + 0.5
            if pc_info.year == 2018:
                pc["score"] = pc["score"] + 0.4
            if pc_info.year == 2017:
                pc["score"] = pc["score"] + 0.3

    #计算用途得分
    #routine    .. professional demands ...  enjoyment
    if "routine" in functions:
        #如果是完成日常办公，轻薄型笔记本加分0.3, 游戏本+0.2,高端本、开发本+0.35,商务本+0.5
        scores_type.append('routine_type')
        for pc in pc_score:
            id = pc["id"]
            pc_info = models.computer.objects.get(id = id)
            if pc_info.type == 'Q':
                pc["score"] = pc["score"] + 0.3
            elif pc_info.type == 'Y':
                pc["score"] = pc["score"] + 0.2
            elif pc_info.type == 'S':
                pc["score"] = pc["score"] + 0.5
            else:
                pc["score"] = pc["score"] + 0.4

    if "professional demands" in functions:
        #如果是专业需求，高端本和开发本加0.5,商务本+0.3，游戏本+0.55
        scores_type.append('professional_demands_score')
        for pc in pc_score:
            id = pc["id"]
            pc_info = models.computer.objects.get(id=id)
            if pc_info.type == "G" or pc_info.type == 'K':
                pc["score"] = pc["score"] + 0.5
            if pc_info.type == "S":
                pc["score"] = pc["score"] + 0.3
            if pc_info.type == 'Y':
                pc["score"] = pc["score"] + 0.55

    if "enjoyment" in functions:
        scores_type.append("enjoyment_score")
        for pc in pc_score:
            id = pc["id"]
            pc_info = models.computer.objects.get(id=id)
            if pc_info.type == 'Y':
                pc["score"] = pc["score"] + 0.5

    # 根据经济投入再做进一步计算
    if expense == "much":
        scores_type.append("price_score")
        for pc in pc_score:
            id = pc["id"]
            pc_info = models.computer.objects.get(id=id)
            pc["score"] = pc["score"] + pc_info.price_score

    sorted_score = sorted(pc_score,key = lambda pc_score:pc_score['score'],reverse = True)
    """
    print("排名前十：")
    print(sorted_score[0]["name"],sorted_score[0]["score"])
    print(sorted_score[1]["name"], sorted_score[1]["score"])
    print(sorted_score[2]["name"], sorted_score[2]["score"])
    print(sorted_score[3]["name"], sorted_score[3]["score"])
    print(sorted_score[4]["name"], sorted_score[4]["score"])
    print(sorted_score[5]["name"], sorted_score[5]["score"])
    print(sorted_score[6]["name"], sorted_score[6]["score"])
    print(sorted_score[7]["name"],sorted_score[7]["score"])
    print(sorted_score[8]["name"], sorted_score[8]["score"])
    print(sorted_score[9]["name"], sorted_score[9]["score"])
    print(sorted_score[10]["name"], sorted_score[10]["score"])
    """
    #这里要进行筛选，选出5个得分最高的，并且名称不同的
    id_list = [] # 5款电脑的型号
    name_list = []
    count = 0
    overall_scores = []

    top5 = []

    for i in range(len(sorted_score)):
        if sorted_score[i]["name"] not in name_list:
            top5.append(sorted_score[i])
            count += 1
            name_list.append(sorted_score[i]["name"])
            id_list.append(sorted_score[i]["id"])
            overall_scores.append(sorted_score[i]["score"])
        if count == 5:
            break

    #以词典方式将后端数据传入前端
    id_1st,id_2nd,id_3rd,id_4th,id_5th = id_list[0], id_list[1],id_list[2],id_list[3],id_list[4]
    pc_set1 = models.computer.objects.filter(id=id_1st)
    pc_set2 = models.computer.objects.filter(id=id_2nd)
    pc_set3 = models.computer.objects.filter(id=id_3rd)
    pc_set4 = models.computer.objects.filter(id=id_4th)
    pc_set5 = models.computer.objects.filter(id=id_5th)
    pc_set = pc_set1 | pc_set2 | pc_set3 | pc_set4 | pc_set5

    #照片集合
    name1,name2,name3,name4,name5 = pc_set1[0].name,pc_set2[0].name,pc_set3[0].name,pc_set4[0].name,pc_set5[0].name
    img1 = models.computerImage.objects.filter(name=name1)
    img2 = models.computerImage.objects.filter(name=name2)
    img3 = models.computerImage.objects.filter(name=name3)
    img4 = models.computerImage.objects.filter(name=name4)
    img5 = models.computerImage.objects.filter(name=name5)
    img_set = img1 | img2 | img3 | img4 | img5

    #computer_rawdata计算机原始数据集合
    pc_s1 = models.computer_rawdata.objects.filter(id=id_1st)
    pc_s2 = models.computer_rawdata.objects.filter(id=id_2nd)
    pc_s3 = models.computer_rawdata.objects.filter(id=id_3rd)
    pc_s4 = models.computer_rawdata.objects.filter(id=id_4th)
    pc_s5 = models.computer_rawdata.objects.filter(id=id_5th)
    raw_data = pc_s1 | pc_s2 | pc_s3 | pc_s4 | pc_s5

    #将score_butter传送给前端 - 先执行清空操作
    buffer = models.score_buffer.objects.all()
    buffer.delete()
    print(scores_type)
    for id in id_list:
        overall_score = overall_scores[id_list.index(id)]
        pc_info = models.computer.objects.get(id=id)
        routine_score,professional_score , price_score,enjoyment_score,year_score,battery_score,beauty_score,disk_score,processor_score,screen_score ,size_score= 0,0,0,0,0,0,0,0,0,0,0
        #['no demand','screen','big_size','battery','disk','strong performance']
        if 'screen_score' in scores_type:
            screen_score = pc_info.screen_score
        if 'size_score' in scores_type:
            size_score = pc_info.size_score
        if 'battery_score' in scores_type:
            battery_score = pc_info.battery_score
        if 'disk_score' in scores_type:
            disk_score = pc_info.disk_score
        if 'processor_score' in scores_type:
            processor_score = pc_info.processor_score
        if 'beauty_score' in scores_type:
            beauty_score = pc_info.beauty_score
        if 'newtype_score' in scores_type:
            if pc_info.year == 2019:
                year_score = 0.5
            elif pc_info.year == 2018:
                year_score = 0.4
            elif pc_info.year == 2018:
                year_score = 0.3
        if 'routine_type' in scores_type:
            if pc_info.type == 'Q':
                routine_score = 0.3
            elif pc_info.type == 'Y':
                routine_score = 0.2
            elif pc_info.type == 'S':
                routine_score = 0.5
            elif pc_info.type == 'G':
                routine_score = 0.4
            else : #开发本
                routine_score = 0.4
        if 'professional_demands_score' in scores_type:
            if pc_info.type == 'Y':
                professional_score = 0.55
            elif pc_info.type == 'G' or pc_info.type == 'K':
                professional_score = 0.5
            elif pc_info.type == 'S':
                professional_score = 0.3
        if 'price_score' in scores_type:
            price_score = pc_info.price_score
        if 'enjoyment_score' in scores_type:
            if pc_info.type == 'Y':
                enjoyment_score = 0.5
        overall_score = round(overall_score,5)
        new_buffer = models.score_buffer(id = id,routine_score = routine_score,professional_score = professional_score,price_score = price_score,enjoyment_score = enjoyment_score,year_score
                                         = year_score,battery_score = battery_score,beauty_score = beauty_score,disk_score = disk_score,processor_score = processor_score,screen_score = screen_score,
                                         size_score = size_score,overall_score = overall_score)
        new_buffer.save()
    buffer = models.score_buffer.objects.all()
    print(buffer.count())

    #for buf in buffer:
        #print(buf.routine_score,buf.professional_score,buf.price_score,buf.enjoyment_score,buf.year_score,buf.battery_score,buf.beauty_score,buf.disk_score,buf.processor_score,buf.screen_score,size_score,overall_score)


    return render(request,'mainpart/recommend.html',{"id_list":id_list,"pc_set":pc_set,"buffer":buffer,"raw_data":raw_data,"img_set":img_set})

def show_all(request):
    pcs = models.computerImage.objects.all()
    pc_name = models.computer.objects.all()
    return render(request,'mainpart/show_all.html',{"pcs":pcs,"pc_name":pc_name})