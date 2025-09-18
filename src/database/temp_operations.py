# from db_session import get_db
# from crud import ORM_CRUD


# with session_pool() as session:
#     ops=ORM_CRUD(session)

#     ops.add_todo(
#         id="JFHKFHJL69X2P",
#         title="Finance report",
#         description="Complete the finance report for xyz product and send it to manager",
#         status="in-progress",
#         priority="high",
#         tags={"type": "work", "urgent": "yes"},
#         due_date="2025-10-07 13:25:41",
#     )

#     result = ops.get_todo_by_key("id","U9369X2P")

#     # print(f"""
#     #       ---------------------------------
#     #       Created At: {result.created_at}
#     #       Updated At: {result.updated_at}
#     #       Due Date: {result.due_date}
#     #       Title: {result.title}
#     #       Description: {result.description}
#     #       Status: {result.status}
#     #       Priority: {result.priority}
#     #       Tags: {result.tags}
#     #       User ID: {result.owner_id}
#     #       ID: {result.id}
#     #       ---------------------------------
#     #       """)
    
#     # results = ops.get_todo_by_title("Finance")

#     # for result in results:

#     #     print(f"""
#     #         ---------------------------------
#     #         Created At: {result.created_at}
#     #         Updated At: {result.updated_at}
#     #         Due Date: {result.due_date}
#     #         Title: {result.title}
#     #         Description: {result.description}
#     #         Status: {result.status}
#     #         Priority: {result.priority}
#     #         Tags: {result.tags}
#     #         User ID: {result.owner_id}
#     #         ID: {result.id}
#     #         ---------------------------------
#             # """)
#     # ops.update_todo("U9369X2P","less")


#     # ops.delete_todo("JFHKFHJL69X2P")
    