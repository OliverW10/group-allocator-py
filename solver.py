from ortools.sat.python import cp_model
import pandas as pd

def assign_students_to_projects(
    students,
    projects,
    student_preferences,
    contract_willing_students,
    contract_required_projects,
    client_projects,
    pre_allocations,
    min_group_size=3,
    max_group_size=4
):
    """
    Assign students to projects based on preferences and constraints.
    
    Parameters:
    - students: List of student IDs
    - projects: List of project IDs
    - student_preferences: Dict mapping student IDs to ordered list of preferred project IDs
    - contract_willing_students: List of student IDs willing to sign contracts
    - contract_required_projects: List of project IDs requiring contracts
    - client_projects: Dict mapping client IDs to list of their project IDs
    - pre_allocations: Dict mapping project IDs to list of pre-allocated student IDs
    - min_group_size: Minimum number of students per project
    - max_group_size: Maximum number of students per project
    
    Returns:
    - Dictionary mapping project IDs to list of assigned student IDs
    - Overall preference satisfaction score
    """
    model = cp_model.CpModel()
    
    # Create variables
    # x[s, p] = 1 if student s is assigned to project p, 0 otherwise
    x = {}
    for s in students:
        for p in projects:
            x[s, p] = model.NewBoolVar(f'x_{s}_{p}')
    
    # y[p] = 1 if project p is selected (has students), 0 otherwise
    y = {}
    for p in projects:
        y[p] = model.NewBoolVar(f'y_{p}')
    
    # Constraint: Each student is assigned to exactly one project
    for s in students:
        model.Add(sum(x[s, p] for p in projects) == 1)
    
    # Constraint: Project is selected if and only if it has at least 1 student
    for p in projects:
        # If project has students, it must be selected
        model.Add(sum(x[s, p] for s in students) >= y[p])
        # If project is selected, it must have students
        model.Add(sum(x[s, p] for s in students) <= max_group_size * y[p])
    
    # Constraint: Each group must have min_group_size to max_group_size people
    for p in projects:
        # Only apply size constraints if project is selected
        student_count = sum(x[s, p] for s in students)
        # If project is selected, it must meet size requirements
        model.Add(student_count >= min_group_size).OnlyEnforceIf(y[p])
        model.Add(student_count <= max_group_size).OnlyEnforceIf(y[p])
    
    # Constraint: Only contract-willing students can be assigned to contract-required projects
    for s in students:
        if s not in contract_willing_students:
            for p in contract_required_projects:
                model.Add(x[s, p] == 0)
    
    # Constraint: For each client, at most one of their projects can run
    for client, client_project_list in client_projects.items():
        model.Add(sum(y[p] for p in client_project_list) <= 1)
    
    # Constraint: Pre-allocated students must be assigned to specific projects
    for p, pre_allocated_students in pre_allocations.items():
        for s in pre_allocated_students:
            model.Add(x[s, p] == 1)
    
    # Objective: Maximize preference satisfaction
    # Lower rank (higher preference) gets higher score
    preference_weights = {1: 10, 2: 9, 3: 8, 4: 7, 5: 6, 
                          6: 5, 7: 4, 8: 3, 9: 2, 10: 1}
    
    objective_terms = []
    for s in students:
        for rank, p in enumerate(student_preferences.get(s, []), 1):
            if rank <= 10 and p in projects:
                objective_terms.append(x[s, p] * preference_weights.get(rank, 0))
    
    model.Maximize(sum(objective_terms))
    
    # Solve the model
    solver = cp_model.CpSolver()
    status = solver.Solve(model)
    
    if status == cp_model.OPTIMAL or status == cp_model.FEASIBLE:
        # Extract solution
        assignments = {p: [] for p in projects}
        for s in students:
            for p in projects:
                if solver.Value(x[s, p]) == 1:
                    assignments[p].append(s)
        
        # Calculate preference satisfaction score
        total_score = 0
        for s in students:
            for rank, p in enumerate(student_preferences.get(s, []), 1):
                if rank <= 10 and p in projects and solver.Value(x[s, p]) == 1:
                    total_score += preference_weights.get(rank, 0)
        
        # Remove empty projects
        assignments = {p: students_list for p, students_list in assignments.items() if students_list}
        
        return assignments, total_score
    else:
        return None, 0

# Example usage
if __name__ == "__main__":
    # Sample data
    students = ["s1", "s2", "s3", "s4", "s5", "s6", "s7", "s8", "s9", "s10", "s11", "s12"]
    
    projects = ["p1", "p2", "p3", "p4", "p5"]
    
    # Top 10 preferences for each student (ordered)
    student_preferences = {
        "s1": ["p1", "p2", "p3", "p4", "p5"],
        "s2": ["p2", "p1", "p3", "p5", "p4"],
        "s3": ["p3", "p1", "p2", "p4", "p5"],
        "s4": ["p1", "p3", "p2", "p5", "p4"],
        "s5": ["p2", "p3", "p1", "p4", "p5"],
        "s6": ["p3", "p2", "p1", "p5", "p4"],
        "s7": ["p4", "p5", "p1", "p2", "p3"],
        "s8": ["p5", "p4", "p2", "p3", "p1"],
        "s9": ["p4", "p3", "p5", "p1", "p2"],
        "s10": ["p5", "p2", "p4", "p3", "p1"],
        "s11": ["p1", "p4", "p5", "p2", "p3"],
        "s12": ["p2", "p5", "p1", "p3", "p4"]
    }
    
    # Students willing to sign contracts
    contract_willing_students = ["s1", "s3", "s5", "s7", "s9", "s11"]
    
    # Projects requiring contracts
    contract_required_projects = ["p1", "p3"]
    
    # Projects from the same client
    client_projects = {
        "client1": ["p1", "p2"],
        "client2": ["p3", "p4"]
    }
    
    # Pre-allocations
    pre_allocations = {
        "p5": ["s8", "s10"]
    }
    
    # Run the assignment
    assignments, score = assign_students_to_projects(
        students=students,
        projects=projects,
        student_preferences=student_preferences,
        contract_willing_students=contract_willing_students,
        contract_required_projects=contract_required_projects,
        client_projects=client_projects,
        pre_allocations=pre_allocations
    )
    
    # Print results
    print(f"Total preference satisfaction score: {score}")
    print("\nProject assignments:")
    for p, assigned_students in assignments.items():
        print(f"{p}: {', '.join(assigned_students)}")
    
    # Print statistics
    print("\nPreference statistics:")
    pref_stats = {i: 0 for i in range(1, 11)}
    pref_stats["unpreferred"] = 0
    
    for s in students:
        assigned = False
        for p in assignments:
            if s in assignments[p]:
                if p in student_preferences[s]:
                    rank = student_preferences[s].index(p) + 1
                    if rank <= 10:
                        pref_stats[rank] += 1
                        assigned = True
                        break
        if not assigned:
            pref_stats["unpreferred"] += 1
    
    for rank, count in pref_stats.items():
        if rank != "unpreferred":
            print(f"Students who got their #{rank} choice: {count}")
        else:
            print(f"Students who got a project not in their top 10: {count}")