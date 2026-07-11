from utils.soft_assert import SoftAssert


def grade_stats_assert(get_grade_response, expected_grade):
    soft = SoftAssert()
    soft.assert_equal(get_grade_response.count,
                      expected_grade.count,
                      f"Get wrong stats count, AR: {get_grade_response.count}, ER: {expected_grade.count}")
    soft.assert_equal(get_grade_response.min,
                      expected_grade.min,
                      f"Get wrong stats min, AR: {get_grade_response.min}, ER: {expected_grade.min}")
    soft.assert_equal(get_grade_response.max,
                      expected_grade.max,
                      f"Get wrong stats max, AR: {get_grade_response.max}, ER: {expected_grade.max}")
    soft.assert_equal(get_grade_response.avg,
                      expected_grade.avg,
                      f"Get wrong stats avg, AR: {get_grade_response.max}, ER: {expected_grade.avg}")
    return soft.assert_all()
