"""
Implement a simple one to one matching algorithm.
"""
def calculate_score(requesting_teacher, potential_swapmate):
    score = 0
    
    # Check TargetLoc for match.
    target_info_req = requesting_teacher.current_info
    target_info_swapmate = potential_swapmate.target_info
    
    if target_info_req and target_info_swapmate: # check if target info is updated
        if (target_info_req.county == target_info_swapmate.county1 and 
            target_info_req.subcounty == target_info_swapmate.subcounty1):
            score += 3  # Highest priority
        elif (target_info_req.county == target_info_swapmate.county2 and 
            target_info_req.subcounty == target_info_swapmate.subcounty2):
            score += 2  # Medium priority
        elif (target_info_req.county == target_info_swapmate.county3 and 
            target_info_req.subcounty == target_info_swapmate.subcounty3):
            score += 1  # Lowest priority
    
    # Conduct a match for secondary school teachers.
    if requesting_teacher.current_info.teaching_level == 'Secondary' and \
    potential_swapmate.current_info.teaching_level == 'Secondary':
        if requesting_teacher.current_info.subject_comb:
            subjects_req = requesting_teacher.current_info.subject_comb
        if potential_swapmate.current_info and \
        potential_swapmate.current_info.subject_comb:
            subjects_swapmate = potential_swapmate.current_info.subject_comb
    
        # score += len(set(subjects_req).intersection(subjects_swapmate))
        if subjects_req and subjects_swapmate:
            if subjects_req == subjects_swapmate: # Same subject comb
                score += 3
        return score
    
    return score


def find_potential_swapmates(requesting_teacher, all_teachers):
    potential_swapmates = []
    for teacher in all_teachers:
        if teacher.current_info and requesting_teacher.current_info:
            if teacher.id != requesting_teacher.id and \
            teacher.current_info.teaching_level == \
                requesting_teacher.current_info.teaching_level:   
                score = calculate_score(requesting_teacher, teacher)
                potential_swapmates.append({'teacher': teacher, 'score': score})
    
    potential_swapmates.sort(key=lambda x: x['score'], reverse=True)
    return potential_swapmates
