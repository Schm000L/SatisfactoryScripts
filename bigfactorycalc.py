
# from enum import Enum
# ItemIDs = Enum('ItemID', 'Iron_Ore Copper_Ore Caterium_Ore Bauxite Quartz Sulfur Oil Water')

# class Item:
#     sharedbyall = 'all'         # class variable shared by all instances

#     def __init__(self, id):
#         self.id = id    # instance variable unique to each instance


import json

f = open ('recipes.json', "r")
RECIPES = dict(json.loads(f.read()))
to_make = []

active_builds = 1
current_build = 0

def handle_requirements(goal_name, goal_amount, level,  recipe_version = "default"):
    global current_build

    if goal_name in RECIPES:
        goal_recipe = RECIPES[goal_name][recipe_version]
        goal_production_ratio = goal_amount/goal_recipe["production"]
        tabs = " "*level
        print(tabs,"Need", round(goal_production_ratio, 2), goal_name, goal_recipe["machine"]+"(s) for", goal_amount, "per min")
        if goal_recipe["requirements"] is not None:
            for r_key, r_val in goal_recipe["requirements"].items():
                rec_version = "alt1" if r_key == "Screw" else "default"
                requirement_recipe = RECIPES[r_key][rec_version]

                r_goal = r_val*goal_production_ratio
                num_machines = r_goal/requirement_recipe["production"]
                if r_key not in to_make[0]:
                    to_make[0][r_key] = {"total": r_goal, "machine": requirement_recipe["machine"], "num_machines": num_machines ,"for_"+goal_name: r_goal}
                else:
                    to_make[0][r_key]["total"] += r_goal
                    num_machines = to_make[0][r_key]["total"]/requirement_recipe["production"]
                    to_make[0][r_key]["num_machines"] = num_machines
                    if "for_"+goal_name not in to_make[0][r_key]:
                        to_make[0][r_key]["for_"+goal_name] = r_goal
                    else:
                        to_make[0][r_key]["for_"+goal_name] += r_goal
                if "by_products" in requirement_recipe and requirement_recipe["by_products"] is not None:
                    for by_key, by_val in requirement_recipe["by_products"].items():
                        if by_key not in to_make[0]:
                            to_make[0][by_key] = {"total": by_val*num_machines, "as_by_product": by_val*num_machines}
                        else:
                            to_make[0][by_key]["total"] += by_val*num_machines
                            if "as_by_product" in to_make[0][by_key]:
                                to_make[0][by_key]["as_by_product"] += by_val*num_machines
                            else:
                                to_make[0][by_key]["as_by_product"] = by_val*num_machines
                handle_requirements(r_key, r_goal, level+1, "alt1" if r_key == "Screw" else "default") # Recursion <3
            
        else:
            print(tabs,"We're at the end!")
    else:
        print("Could not find recipe for", goal_name)

def handle_requirements2(goal_name, goal_amount, level, current_build):
    recipe_version = "default"
    global active_builds

    if goal_name in RECIPES:
        print(RECIPES[goal_name])
        i = 0
        for rcp_id, rcp in RECIPES[goal_name].items():
            print(rcp_id, rcp)
            active_builds+=i
            goal_recipe = RECIPES[goal_name][rcp_id]
            goal_production_ratio = goal_amount/goal_recipe["production"]
            if i == 0:
                to_make[0][rcp_id] = {"total": r_goal, "machine": requirement_recipe["machine"], "num_machines": num_machines ,"for_"+goal_name: r_goal}
            else:
                print("WWAWA")
            i+=1

        goal_recipe = RECIPES[goal_name][recipe_version]
        goal_production_ratio = goal_amount/goal_recipe["production"]
        tabs = " "*level
        print(tabs,"Need", round(goal_production_ratio, 2), goal_name, goal_recipe["machine"]+"(s) for", goal_amount, "per min")
        if False:
            print("a")
        # if goal_recipe["requirements"] is not None:
        #     for r_key, r_val in goal_recipe["requirements"].items():
        #         rec_version = "alt1" if r_key == "Screw" else "default"
        #         requirement_recipe = RECIPES[r_key][rec_version]

        #         r_goal = r_val*goal_production_ratio
        #         num_machines = r_goal/requirement_recipe["production"]
        #         if r_key not in to_make[0]:
        #             to_make[0][r_key] = {"total": r_goal, "machine": requirement_recipe["machine"], "num_machines": num_machines ,"for_"+goal_name: r_goal}
        #         else:
        #             to_make[0][r_key]["total"] += r_goal
        #             num_machines = to_make[0][r_key]["total"]/requirement_recipe["production"]
        #             to_make[0][r_key]["num_machines"] = num_machines
        #             if "for_"+goal_name not in to_make[0][r_key]:
        #                 to_make[0][r_key]["for_"+goal_name] = r_goal
        #             else:
        #                 to_make[0][r_key]["for_"+goal_name] += r_goal
        #         if "by_products" in requirement_recipe and requirement_recipe["by_products"] is not None:
        #             for by_key, by_val in requirement_recipe["by_products"].items():
        #                 if by_key not in to_make[0]:
        #                     to_make[0][by_key] = {"total": by_val*num_machines, "as_by_product": by_val*num_machines}
        #                 else:
        #                     to_make[0][by_key]["total"] += by_val*num_machines
        #                     if "as_by_product" in to_make[0][by_key]:
        #                         to_make[0][by_key]["as_by_product"] += by_val*num_machines
        #                     else:
        #                         to_make[0][by_key]["as_by_product"] = by_val*num_machines
        #         handle_requirements(r_key, r_goal, level+1, "alt1" if r_key == "Screw" else "default") # Recursion <3
            
        else:
            print(tabs,"We're at the end!")
    else:
        print("Could not find recipe for", goal_name)



def main():
    goal = {"Screw": 200}
    
    global to_make
    global active_builds
    global current_build
    to_make.append(dict(goal))

    # Format goal for to_make-dict
    # tmk = to_make[0]

    # cpy = to_make.copy()
    # for tmk in cpy:
    #     for k, v in tmk.items():
    #         count = 0
    #         for recipe_id in RECIPES[k]:
    #             if count == 0:
    #                 print(tmk)
    #                 tmk[k] = {"total": v, "machine": RECIPES[k][recipe_id]["machine"], "num_machines": v/RECIPES[k][recipe_id]["production"]}
    #                 count+=1
    #             else:
    #                 tmp = [dict(tmk)]
    #                 tmp[0][k] = {"total": v, "machine": RECIPES[k][recipe_id]["machine"], "num_machines": v/RECIPES[k][recipe_id]["production"]}
                    
    #                 to_make += tmp
                    # print("Aaa", tmp, to_make, recipe_id)

    # print(to_make)
        # if len(RECIPES[k]) > 1:
        #     for _ in range(len(RECIPES[k])-1):
        #         to_make.append(dict(to_make[current_build]))
        #         active_builds += 1
        #     current_build += 1
        #     for i, j in RECIPES[k].items():
        #         print(i)
        #         print(j)
        # recipe_version = "alt1" if k == "Screw" else "default"
        # to_make[0][k] = {"total": v, "machine": RECIPES[k][recipe_version]["machine"], "num_machines": v/RECIPES[k][recipe_version]["production"]}
    
    # main loop
    for goal_key, goal_value in goal.items():
        print("To produce", goal_value, goal_key + ":")
        handle_requirements2(goal_key, goal_value, 1, 1)
    #     recipe_version = "alt1" if k == "Screw" else "default"
        # handle_requirements(goal_key, goal_value, 1, recipe_version)

    # outfile = open("out.json", "w")
    # outfile.write(json.dumps(to_make))

    # print(to_make)
            



def handle_requirements3(goal_name, goal_amount, level,  recipe_version = "default"):     
            if goal_name in RECIPES:
                goal_recipe = RECIPES[goal_name][recipe_version]
                goal_production_ratio = goal_amount/goal_recipe["production"]
                tabs = " "*level
                print(tabs,"Need", round(goal_production_ratio, 2), goal_name, goal_recipe["machine"]+"(s) for", goal_amount, "per min")
                if goal_recipe["requirements"] is None:
                    print(tabs, "We're at end!")
                    return
                for r_key, r_val in goal_recipe["requirements"].items():
                    rec_version = "alt1" if r_key == "Screw" else "default"
                    requirement_recipe = RECIPES[r_key][rec_version]

                    r_goal = r_val*goal_production_ratio
                    num_machines = r_goal/requirement_recipe["production"]
                    if r_key not in to_make:
                        to_make[r_key] = {"total": r_goal, "machine": requirement_recipe["machine"], "num_machines": num_machines ,"for_"+goal_name: r_goal}
                    else:
                        to_make[r_key]["total"] += r_goal
                        num_machines = to_make[r_key]["total"]/requirement_recipe["production"]
                        to_make[r_key]["num_machines"] = num_machines
                        if "for_"+goal_name not in to_make[r_key]:
                            to_make[r_key]["for_"+goal_name] = r_goal
                        else:
                            to_make[r_key]["for_"+goal_name] += r_goal
                    if "by_products" in requirement_recipe and requirement_recipe["by_products"] is not None:
                        for by_key, by_val in requirement_recipe["by_products"].items():
                            if by_key not in to_make:
                                to_make[by_key] = {"total": by_val*num_machines, "as_by_product": by_val*num_machines}
                            else:
                                to_make[by_key]["total"] += by_val*num_machines
                                if "as_by_product" in to_make[by_key]:
                                    to_make[by_key]["as_by_product"] += by_val*num_machines
                                else:
                                    to_make[by_key]["as_by_product"] = by_val*num_machines
                    handle_requirements(r_key, r_goal, level+1, "alt1" if r_key == "Screw" else "default") # Recursion <3
                    
            else:
                print("Could not find recipe for", goal_name)




if __name__ == "__main__":
    main()