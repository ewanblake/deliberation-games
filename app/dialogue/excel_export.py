import os

from artifact_tool import Workbook, SpreadsheetFile

def calculate_dialogue_statistics(engine, dialogue_id):

    move_counts = {
        "PROPOSE": 0,
        "SUPPORT": 0,
        "CHALLENGE": 0,
        "ACCEPT": 0,
        "REJECT": 0,
        "WITHDRAW": 0
    }

    burden_counts = {
        "CREATED": 0,
        "ACTIVATED": 0,
        "SATISFIED": 0,
        "RESOLVED": 0
    }

    for turn in engine.transcript.turns:

        move = turn.get("move")

        if move in move_counts:
            move_counts[move] += 1

        burden_event = turn.get(
            "burden_event"
        )

        if burden_event in burden_counts:
            burden_counts[burden_event] += 1

    termination_reason = (
        engine.termination_reason
        or "UNKNOWN"
    )

    accepted_flag = (
        1
        if termination_reason == "PROPOSAL_ACCEPTED"
        else 0
    )

    rejected_flag = (
        1
        if termination_reason == "PROPOSAL_REJECTED"
        else 0
    )

    accepted_proposal = None

    if accepted_flag == 1:
        accepted_proposal = (
            engine.current_proposal
        )

    return[
        dialogue_id,
        engine.protocol,
        len(engine.transcript.turns),
        termination_reason,
        termination_reason,
        accepted_proposal,
        move_counts["PROPOSE"],
        move_counts["SUPPORT"],
        move_counts["CHALLENGE"],
        move_counts["ACCEPT"],
        move_counts["REJECT"],
        move_counts["WITHDRAW"],
        burden_counts["CREATED"],
        burden_counts["ACTIVATED"],
        burden_counts["SATISFIED"],
        burden_counts["RESOLVED"],
        accepted_flag,
        rejected_flag

    ]

def get_next_results_filename():

    folder = "app/results"

    os.makedirs(
        folder,
        exist_ok=True
    )

    existing_files = [
        filename
        for filename in os.listdir(folder)
        if (
            filename.startswith(
                "simulation_results_"
            )
            and filename.endswith(
                ".xlsx"
            )
        )
    ]

    next_number = (
        len(existing_files) + 1
    )

    return os.path.join(
        folder,
        f"simulation_results_{next_number:03}.xlsx"
    )

def export_comparative_results(
        standard_engines,
        burden_engines
):

    workbook = Workbook.create()

    raw_sheet = workbook.worksheets.add(
        "Raw Data"
    )

    summary_sheet = workbook.worksheets.add(
        "Protocol Summary"
    )

    headers = [
        "Dialogue ID",
        "Protocol",
        "Turn Count",
        "Outcome",
        "Termination Reason",
        "Accepted Proposal",
        "PROPOSE",
        "SUPPORT",
        "CHALLENGE",
        "ACCEPT",
        "REJECT",
        "WITHDRAW",
        "Burdens Created",
        "Burdens Activated",
        "Burdens Satisfied",
        "Burdens Resolved"<
        "Accepted Flag",
        "Rejected Flag"
    ]

    rows = []

    dialogue_id = 1

    for engine in standard_engines:

        rows.append(
            calculate_dialogue_statistics(
                engine,
                dialogue_id
            )
        )

        dialogue_id += 1

    for engine in burden_engines:

        rows.append(
            calculate_dialogue_statistics(
                engine,
                dialogue_id
            )
        )

        dialogue_id += 1


    raw_sheet.get_range(
        "A1:R1"
    ).values = [
        headers
    ]

    if rows:

        end_row = len(rows) + 1

        raw_sheet.get_range(
            f"A2:R{end_row}"
        ).values = rows

    else:

        end_row = 2

    raw_sheet.freeze_panes.freeze_rows(
        1
    )

    raw_sheet.get_range(
        "A1:R1"
    ).format = {
        "fill": "#111827",
        "font": {
            "bold": True,
            "color": "#FFFFFF"
        },
        "horizontal_alignment": "center",
        "vertical_alignment": "center",
        "wrap_text": True
    }

    raw_sheet.get_range(
        f"A1:R{end_row}"
    ).format.wrap_text = True

    raw_sheet.get_range(
        f"A1:R{end_row}"
    ).format.autofit_columns()

    raw_sheet.get_range(
        "D:F"
    ).format.column_width

    summary_headers = [
        "Protocol",
        "Dialogues",
        "Average Turns",
        "Acceptance Rate",
        "Rejection Rate",
        "Average Proposals",
        "Average Supports",
        "Average Challenges",
        "Average Withdrawals",
        "Burdens Created",
        "Burdens Activated",
        "Burdens Satisfied",
        "Burdens Resolved",
        "Burden Satisfaction Rate"
    ]

    summary_sheet.get_range(
        "A1:N1"
    ).values = [
        summary_headers
    ]

    summary_sheet.get_range(
        "A2:A3"
    ).values = [
        ["Standard"],
        ["Burden"]
    ]

    summary_sheet.get_range(
        "B2"
    ).formulas = [[
        (
            f'COUNTIF('
            f"'Raw Data'!£B$2:$B${end_row},"
            f'A2)'
        )
    ]]

    summary_sheet.get_range(
        "B2:B3"
    ).fill_down()

    summary_sheet.get_range(
        "C2"
    ).formulas = [[
        (
            f'AVERAGEIF('
            f"'Raw Data'!$B$2:$B${end_row},"
            f'A2,'
            f"'Raw Data'!$C$2:$C${end_row})"
        )
    ]]

    summary_sheet.get_range(
        "C2:C3"
    ).fill_down()

    summary_sheet.get_range(
        "D2"
    ).formulas = [[
        (
            f'=IF(B2=0,0,'
            f'SUMIF(',
            f"'Raw Data'!B$2:$B${end_row},"
            f'A2,'
            f"'Raw Data'!$Q$2:$Q${end_row})"
            f'/B2)'
        )
    ]]

    summary_sheet.get_range(
        "D2:D3"
    ).fill_down()

    summary_sheet.get_range(
        "E2"
    ).formulas = [[
        (
            f'=IF(B2=0,0,'
            f'SUMIF('
            f"'Raw Data'!$B$2:$B${end_row},"
            f'A2,'
            f"'Raw Data'!$R$2:$R${end_row})"
            f'/B2)'
        )
    ]]

    summary_sheet.get_range(
        "E2:E3"
    ).fill_down()
    
    summary_sheet.get_range(
        "F2"
    ).formulas = [[
        (
            f'=AVERAGEIF('
            f"'Raw Data'!$B$2:$B${end_row},"
            f'A2,'
            f"'Raw Data'!$G$2:$G${end_row})"
        )
    ]]

    summary_sheet.get_range(
        "F2:F3"
    ).fill_down()
        
    summary_sheet.get_range(
        "G2"
    ).formulas = [[
        (
            f'=AVERAGEIF('
            f"'Raw Data'!$B$2:$B${end_row},"
            f'A2,'
            f"'Raw Data'!$H$2:$H${end_row})"
        )
    ]]

    summary_sheet.get_range(
        "G2:G3"
    ).fill_down()
            
    summary_sheet.get_range(
        "H2"
    ).formulas = [[
        (
            f'=AVERAGEIF('
            f"'Raw Data'!$B$2:$B${end_row},"
            f'A2,'
            f"'Raw Data'!$I$2:$I${end_row})"
        )
    ]]

    summary_sheet.get_range(
        "H2:H3"
    ).fill_down()
        
    summary_sheet.get_range(
        "I2"
    ).formulas = [[
        (
            f'=AVERAGEIF('
            f"'Raw Data'!$B$2:$B${end_row},"
            f'A2,'
            f"'Raw Data'!$L$2:$L${end_row})"
        )
    ]]

    summary_sheet.get_range(
        "I2:I3"
    ).fill_down()
        
    summary_sheet.get_range(
        "J2"
    ).formulas = [[
        (
            f'=SUMIF('
            f"'Raw Data'!$B$2:$B${end_row},"
            f'A2,'
            f"'Raw Data'!$M$2:$M${end_row})"
        )
    ]]

    summary_sheet.get_range(
        "J2:J3"
    ).fill_down()
        
    summary_sheet.get_range(
        "K2"
    ).formulas = [[
        (
            f'=SUMIF('
            f"'Raw Data'!$B$2:$B${end_row},"
            f'A2,'
            f"'Raw Data'!$N$2:$N${end_row})"
        )
    ]]

    summary_sheet.get_range(
        "K2:K3"
    ).fill_down()
        
    summary_sheet.get_range(
        "L2"
    ).formulas = [[
        (
            f'=SUMIF('
            f"'Raw Data'!$B$2:$B${end_row},"
            f'A2,'
            f"'Raw Data'!$O$2:$O${end_row})"
        )
    ]]

    summary_sheet.get_range(
        "L2:L3"
    ).fill_down()
        
    summary_sheet.get_range(
        "M2"
    ).formulas = [[
        (
            f'=SUMIF('
            f"'Raw Data'!$B$2:$B${end_row},"
            f'A2,'
            f"'Raw Data'!$P$2:$P${end_row})"
        )
    ]]

    summary_sheet.get_range(
        "M2:M3"
    ).fill_down()

    summary_sheet.get_range(
        "N2"
    ).formulas = [[
        '=IF(K2=0,0,L2/K2)'
    ]]

    summary_sheet.get_range(
        "N2:N3"
    ).fill_down()

    summary_sheet.get_range(
        "A1:N1"
    ).format = {
        "fill": "#111827",
        "font": {
            "bold": True,
            "color": "#FFFFFF"
        },
        "horizontal_alignment": "center",
        "vertical_alignment": "center",
        "wrap_text": True
    }

    summary_sheet.get_range(
        "A1:N3"
    ).format.autofit_columns()

    summary_sheet.get_range(
        "D2:E3"
    ).format.number_format = "0.00%"

    summary_sheet.get_range(
        "N2:N3"
    ).format.number_format = "0.00%"

    summary_sheet.get_range(
        "C2:I3"
    ).format.number_format = "0.00%"

    output_path = (
        get_next_results_filename()
    )

    SpreadsheetFile.export_xlsx(
        workbook
    ).save(
        output_path
    )

    print()
    print(
        f"Excel results exported to: "
        f"{output_path}"
    )

    return output_path


    

    

