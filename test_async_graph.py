import asyncio
import aiosqlite
from langgraph.checkpoint.sqlite.aio import AsyncSqliteSaver
from langgraph.graph import StateGraph
import typing

async def main():
    db_conn = await aiosqlite.connect("test_checkpoints.sqlite")
    memory = AsyncSqliteSaver(db_conn)
    
    class State(typing.TypedDict):
        count: int
        
    def add_one(state: State):
        return {"count": state["count"] + 1}
        
    builder = StateGraph(State)
    builder.add_node("adder", add_one)
    builder.set_entry_point("adder")
    builder.set_finish_point("adder")
    
    graph = builder.compile(checkpointer=memory)
    
    config = {"configurable": {"thread_id": "test_1"}}
    async for output in graph.astream({"count": 1}, config=config):
        print(output)
        
    history = []
    async for s in graph.aget_state_history(config):
        history.append(s.values)
    print("History:", history)
    
    await db_conn.close()

if __name__ == "__main__":
    asyncio.run(main())
