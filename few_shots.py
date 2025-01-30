from langchain_experimental.sql import SQLDatabaseChain

#
# def create_few_shots(llm, db):
#  PROMPT = """
#      Given an input question, first create a syntactically correct mysql query to run,
#      then look at the results of the query and return the answer. The output should include only the query and nothing else.
#      The question: {question}
#      """
#
#  # Define the BaseCache placeholder
#  class BaseCache:
#   pass
#
#  class Callbacks:
#   pass
#
#  #
#
#  # Rebuild the Pydantic model
#  SQLDatabaseChain.model_rebuild()
#
#  db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True, top_k=3)
#
#  qns1 = db_chain.run(PROMPT.format(question="""SELECT r.product_category, SUM(r.revenue_amount) - COALESCE(SUM(e.expense_amount), 0) AS net_revenue
#                                                  FROM revenue r LEFT JOIN expenses e ON r.product_category = e.expense_type
#                                                  AND YEAR(r.revenue_date) = YEAR(e.expense_date) WHERE YEAR(r.revenue_date) = 2023
#                                                  GROUP BY r.product_category
#                                                  ORDER BY net_revenue DESC
#                                                  LIMIT 1;"""))
#
#  qns2 = db_chain.run(PROMPT.format(question="""WITH MonthlyExpenses AS (
#          SELECT
#              expense_type,
#              MONTH(expense_date) AS expense_month,
#              SUM(expense_amount) AS total_expense,
#              RANK() OVER (PARTITION BY MONTH(expense_date) ORDER BY SUM(expense_amount) DESC) AS expense_rank
#          FROM expenses
#          WHERE YEAR(expense_date) = 2023
#          GROUP BY expense_type, MONTH(expense_date)
#      )
#      SELECT expense_type, expense_month, total_expense
#      FROM MonthlyExpenses
#      WHERE expense_rank <= 3;
#      """))
#
#  qns3 = db_chain.run(PROMPT.format(question="""WITH MonthlyProductRevenue AS (
#          SELECT
#              product_name,
#              MONTH(revenue_date) AS revenue_month,
#              SUM(revenue_amount) AS total_revenue,
#              RANK() OVER (PARTITION BY MONTH(revenue_date) ORDER BY SUM(revenue_amount) DESC) AS revenue_rank
#          FROM revenue
#          WHERE YEAR(revenue_date) = 2023
#          GROUP BY product_name, MONTH(revenue_date)
#      )
#      SELECT product_name, revenue_month, total_revenue
#      FROM MonthlyProductRevenue
#      WHERE revenue_rank = 1;
#      """))
#
#  qns4 = db_chain.run(PROMPT.format(question="""WITH MonthlyExpenses AS (
#          SELECT
#              expense_type,
#              MONTH(expense_date) AS expense_month,
#              SUM(expense_amount) AS total_expense,
#              RANK() OVER (PARTITION BY MONTH(expense_date) ORDER BY SUM(expense_amount) DESC) AS expense_rank
#          FROM expenses
#          WHERE YEAR(expense_date) = 2023
#          GROUP BY expense_type, MONTH(expense_date)
#      )
#      SELECT expense_type, expense_month, total_expense
#      FROM MonthlyExpenses
#      WHERE expense_rank <= 3;
#      """))
#
#  qns5 = db_chain.run(PROMPT.format(question="""WITH MonthlyProductRevenue AS (
#          SELECT
#              product_name,
#              MONTH(revenue_date) AS revenue_month,
#              SUM(revenue_amount) AS total_revenue,
#              RANK() OVER (PARTITION BY MONTH(revenue_date) ORDER BY SUM(revenue_amount) DESC) AS revenue_rank
#          FROM revenue
#          WHERE YEAR(revenue_date) = 2023
#          GROUP BY product_name, MONTH(revenue_date)
#      )
#      SELECT product_name, revenue_month, total_revenue
#      FROM MonthlyProductRevenue
#      WHERE revenue_rank = 1;
#
#      """))
#
#  few_shots = [
#   {
#    'Question': "What is the top-performing product category in terms of net revenue (total revenue - total expense) in 2023?",
#    'SQLQuery': """SELECT r.product_category, SUM(r.revenue_amount) - COALESCE(SUM(e.expense_amount), 0) AS net_revenue
#                      FROM revenue r LEFT JOIN expenses e ON r.product_category = e.expense_type
#                      AND YEAR(r.revenue_date) = YEAR(e.expense_date) WHERE YEAR(r.revenue_date) = 2023
#                      GROUP BY r.product_category
#                      ORDER BY net_revenue DESC
#                      LIMIT 1;""",
#    'SQLResult': "Result of the SQL query",
#    'Answer': qns1},
#
#   {'Question': "What are the top 3 expense categories by total amount for each month in 2023?",
#    'SQLQuery': """WITH MonthlyExpenses AS (
#      SELECT
#          expense_type,
#          MONTH(expense_date) AS expense_month,
#          SUM(expense_amount) AS total_expense,
#          RANK() OVER (PARTITION BY MONTH(expense_date) ORDER BY SUM(expense_amount) DESC) AS expense_rank
#      FROM expenses
#      WHERE YEAR(expense_date) = 2023
#      GROUP BY expense_type, MONTH(expense_date)
#  )
#  SELECT expense_type, expense_month, total_expense
#  FROM MonthlyExpenses
#  WHERE expense_rank <= 3;
#  """,
#    'SQLResult': "Result of the SQL query",
#    'Answer': qns2},
#
#   {'Question': "Which product generated the most revenue in each month of 2023?",
#    'SQLQuery': """WITH MonthlyProductRevenue AS (
#      SELECT
#          product_name,
#          MONTH(revenue_date) AS revenue_month,
#          SUM(revenue_amount) AS total_revenue,
#          RANK() OVER (PARTITION BY MONTH(revenue_date) ORDER BY SUM(revenue_amount) DESC) AS revenue_rank
#      FROM revenue
#      WHERE YEAR(revenue_date) = 2023
#      GROUP BY product_name, MONTH(revenue_date)
#  )
#  SELECT product_name, revenue_month, total_revenue
#  FROM MonthlyProductRevenue
#  WHERE revenue_rank = 1;
#  """,
#    'SQLResult': "Result of the SQL query",
#    'Answer': qns3},
#
#   {'Question': "Which expense categories had the highest total expenses for each month in 2023?",
#    'SQLQuery': """WITH MonthlyExpenses AS (
#      SELECT
#          expense_type,
#          MONTH(expense_date) AS expense_month,
#          SUM(expense_amount) AS total_expense,
#          RANK() OVER (PARTITION BY MONTH(expense_date) ORDER BY SUM(expense_amount) DESC) AS expense_rank
#      FROM expenses
#      WHERE YEAR(expense_date) = 2023
#      GROUP BY expense_type, MONTH(expense_date)
#  )
#  SELECT expense_type, expense_month, total_expense
#  FROM MonthlyExpenses
#  WHERE expense_rank <= 3;
#  """,
#    'SQLResult': "Result of the SQL query",
#    'Answer': qns4},
#
#   {'Question': "Which product had the highest revenue in each month of 2023?",
#    'SQLQuery': """WITH MonthlyProductRevenue AS (
#      SELECT
#          product_name,
#          MONTH(revenue_date) AS revenue_month,
#          SUM(revenue_amount) AS total_revenue,
#          RANK() OVER (PARTITION BY MONTH(revenue_date) ORDER BY SUM(revenue_amount) DESC) AS revenue_rank
#      FROM revenue
#      WHERE YEAR(revenue_date) = 2023
#      GROUP BY product_name, MONTH(revenue_date)
#  )
#  SELECT product_name, revenue_month, total_revenue
#  FROM MonthlyProductRevenue
#  WHERE revenue_rank = 1;
#  """,
#    'SQLResult': "Result of the SQL query",
#    'Answer': qns5
#    }
#  ]
#
#  return few_shots







# ----------------

from langchain_experimental.sql import SQLDatabaseChain

# Define a function to initialize and cache the db_chain and few_shots
class FewShotsCache:
    def __init__(self):
        self.few_shots = None
        self.db_chain = None

    def initialize_few_shots(self, llm, db):
        if self.few_shots is not None:
            # If few_shots is already computed, return it
            return self.few_shots

        # Prompt template
        PROMPT = """ 
            Given an input question, first create a syntactically correct mysql query to run,  
            then look at the results of the query and return the answer. The output should include only the query and nothing else.  
            The question: {question}
        """

        # Initialize the database chain if not already done
        if self.db_chain is None:
          class BaseCache:
           pass

          class Callbacks:
           pass

          SQLDatabaseChain.model_rebuild()
          self.db_chain = SQLDatabaseChain(llm=llm, database=db, verbose=True, top_k=3)

        # Run the queries once and cache the results
        qns1 = self.db_chain.run(PROMPT.format(question="""SELECT r.product_category, SUM(r.revenue_amount) - COALESCE(SUM(e.expense_amount), 0) AS net_revenue 
                                                           FROM revenue r LEFT JOIN expenses e ON r.product_category = e.expense_type 
                                                           AND YEAR(r.revenue_date) = YEAR(e.expense_date) WHERE YEAR(r.revenue_date) = 2023
                                                           GROUP BY r.product_category 
                                                           ORDER BY net_revenue DESC
                                                           LIMIT 1;"""))
        qns2 = self.db_chain.run(PROMPT.format(question="""WITH MonthlyExpenses AS (
                SELECT 
                    expense_type, 
                    MONTH(expense_date) AS expense_month, 
                    SUM(expense_amount) AS total_expense,
                    RANK() OVER (PARTITION BY MONTH(expense_date) ORDER BY SUM(expense_amount) DESC) AS expense_rank
                FROM expenses
                WHERE YEAR(expense_date) = 2023
                GROUP BY expense_type, MONTH(expense_date)
            )
            SELECT expense_type, expense_month, total_expense
            FROM MonthlyExpenses
            WHERE expense_rank <= 3;
        """))
        qns3 = self.db_chain.run(PROMPT.format(question="""WITH MonthlyProductRevenue AS (
                SELECT 
                    product_name, 
                    MONTH(revenue_date) AS revenue_month, 
                    SUM(revenue_amount) AS total_revenue,
                    RANK() OVER (PARTITION BY MONTH(revenue_date) ORDER BY SUM(revenue_amount) DESC) AS revenue_rank
                FROM revenue
                WHERE YEAR(revenue_date) = 2023
                GROUP BY product_name, MONTH(revenue_date)
            )
            SELECT product_name, revenue_month, total_revenue
            FROM MonthlyProductRevenue
            WHERE revenue_rank = 1;
        """))

        # Precomputed few_shots
        self.few_shots = [
            {
                'Question': "What is the top-performing product category in terms of net revenue (total revenue - total expense) in 2023?",
                'SQLQuery': """SELECT r.product_category, SUM(r.revenue_amount) - COALESCE(SUM(e.expense_amount), 0) AS net_revenue
                                 FROM revenue r LEFT JOIN expenses e ON r.product_category = e.expense_type
                                 AND YEAR(r.revenue_date) = YEAR(e.expense_date) WHERE YEAR(r.revenue_date) = 2023
                                 GROUP BY r.product_category
                                 ORDER BY net_revenue DESC
                                 LIMIT 1;""",
                'SQLResult': "Result of the SQL query",
                'Answer': qns1
            },
            {
                'Question': "What are the top 3 expense categories by total amount for each month in 2023?",
                'SQLQuery': """WITH MonthlyExpenses AS (
                    SELECT
                        expense_type,
                        MONTH(expense_date) AS expense_month,
                        SUM(expense_amount) AS total_expense,
                        RANK() OVER (PARTITION BY MONTH(expense_date) ORDER BY SUM(expense_amount) DESC) AS expense_rank
                    FROM expenses
                    WHERE YEAR(expense_date) = 2023
                    GROUP BY expense_type, MONTH(expense_date)
                )
                SELECT expense_type, expense_month, total_expense
                FROM MonthlyExpenses
                WHERE expense_rank <= 3;
                """,
                'SQLResult': "Result of the SQL query",
                'Answer': qns2
            },
            {
                'Question': "Which product generated the most revenue in each month of 2023?",
                'SQLQuery': """WITH MonthlyProductRevenue AS (
                    SELECT
                        product_name,
                        MONTH(revenue_date) AS revenue_month,
                        SUM(revenue_amount) AS total_revenue,
                        RANK() OVER (PARTITION BY MONTH(revenue_date) ORDER BY SUM(revenue_amount) DESC) AS revenue_rank
                    FROM revenue
                    WHERE YEAR(revenue_date) = 2023
                    GROUP BY product_name, MONTH(revenue_date)
                )
                SELECT product_name, revenue_month, total_revenue
                FROM MonthlyProductRevenue
                WHERE revenue_rank = 1;
                """,
                'SQLResult': "Result of the SQL query",
                'Answer': qns3
            }
        ]

        return self.few_shots







