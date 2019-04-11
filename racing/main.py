from scrapy.NewStaff import NewStaff
from scrapy.NewResult import NewResult


def main():
    new_staff = NewStaff()
    new_staff.jockey_data()
    new_staff.trainer_data()

    newResult = NewResult()
    newResult.result_data()

if __name__ == "__main__":
    main()
