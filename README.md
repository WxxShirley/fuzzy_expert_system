## 开发过程
### 整体结构
![整体结构](https://github.com/WxxShirley/fuzzy_expert_system/blob/master/flowchart/整体结构.png)
* 获取笔记本电脑详细配置参数。共收集了157条笔记本电脑信息（不含大多数游戏本），具体包括品牌、型号、年份、续航时间、是否有独立显卡、处理器、内存、硬盘大小等
* 模糊规则映射。将各参数信息分别映射到[0,1]区间的数值。这里通过Matlab工具箱FuzzyLogic来处理。如评估续航能力，输入为续航时间，输出为续航能力的得分。
  像评估处理器的性能，输入为内存容量、处理器i5/i7、是否有独立显卡、CPU核数，并制定了了一系列规则来评估。
  如：IF 处理器为i7 and 内存容量为 16G , THEN 处理器性能为最佳
     IF 处理器为i5 and 有独立显卡，THEM 处理器性能较好
     IF 处理器为i5 and 内存容量为 8G and 无独立显卡，处理器性能一般。 （实际制订的规则更多，也更复杂）
  * 模糊设计处理
    ![模糊设计处理](https://github.com/WxxShirley/fuzzy_expert_system/blob/master/flowchart/模糊设计处理.png)
* 使用Django开发，前端引导用户填写问卷，选择自己对笔记本电脑的要求（包括用途、对性能如屏幕分辨率、处理器、续航时间等要求、预算）。
  将笔记本电脑原始数据信息和各项得分信息分别存入数据库中，计算时取出，并根据用户的需求与得分做内积运算。最终选取得分较高的前五名（由于同一型号不同配置的
  笔记本电脑得分相近，这里对同一型号仅保留了得分最高的电脑，后期可能会在展示页面增加链接进入同种型号不同配置的电脑的页面）推荐给用户，并展示笔记本电脑
  图片、针对用户需求的指标的得分情况、总推荐指数和其他具体信息。
  * 打分过程
    ![打分过程](https://github.com/WxxShirley/fuzzy_expert_system/blob/master/flowchart/打分过程.png)
  * 数据库设计
    ![数据库](https://github.com/WxxShirley/fuzzy_expert_system/blob/master/flowchart/数据库.png)
  
## 效果图
### example1 - 推荐经济入门款
* 用户选择
![用户输入](https://github.com/WxxShirley/fuzzy_expert_system/blob/master/screenshots/1.jpg)

* 返回推荐结果
![返回推荐结果](https://github.com/WxxShirley/fuzzy_expert_system/blob/master/screenshots/1_response.jpg)

### example2 - 推荐性能好、性价比高
* 用户选择
![用户输入](https://github.com/WxxShirley/fuzzy_expert_system/blob/master/screenshots/2.jpg)

* 返回推荐结果
![返回推荐结果](https://github.com/WxxShirley/fuzzy_expert_system/blob/master/screenshots/2_response_1.jpg)
![返回推荐结果](https://github.com/WxxShirley/fuzzy_expert_system/blob/master/screenshots/2_response_2.jpg)
