1. implement the genetic algorithm . using just cutsize to calculate fitness

   the programme just group all nets to one side of the partition hence the partition is of cause optimal(the cutsize is 0!)

2. using fitness function from the paper. it solves the above problem but often the partition result is not very balanced.

   but the partition result is very unbalanced and the cutsize is often not great even for small benchmarch files

   ![z4ml](report_draft.assets/z4ml.png)![cm82a](report_draft.assets/cm82a.png)

3 it give me great result when I make the population size larger(10 -> 100), and generation time is 100. but it is really slow. it took a long time for small benchmark file like `cm82a`

![cm82a](report_draft.assets/cm150a.png)