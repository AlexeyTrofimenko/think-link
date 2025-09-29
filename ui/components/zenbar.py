import streamlit as st
from agents import ask_agent, do_agent


def _clear_caches() -> None:
    try:
        st.cache_data.clear()
    except Exception:
        pass
    try:
        st.cache_resource.clear()
    except Exception:
        pass


def zenbar(placeholder: str = "Ask or command…") -> None:
    msg = st.chat_input(placeholder)
    if not msg:
        return

    note_id = st.session_state.get("selected_note_id")
    if note_id is None:
        try:
            resp = ask_agent(msg)
            if resp.note_id:
                st.session_state["selected_note_id"] = resp.note_id
            else:
                st.session_state["pending_answer"] = resp.answer
                st.session_state["open_dialog"] = True
        except Exception as e:
            st.session_state["pending_answer"] = f"⚠️ Error: {e}"
            st.session_state["open_dialog"] = True
        finally:
            _clear_caches()
            st.rerun()
    else:
        try:
            resp = do_agent(str(note_id), msg)
            if resp.note_id:
                st.session_state["note_answers"][str(note_id)] = f"Update Note #{resp.note_id}"
            else:
                st.session_state["note_answers"][str(note_id)] = f"{resp.answer}"

        except Exception as e:
            st.session_state["note_answers"][str(note_id)] = f"⚠️ Error: {e}"
        finally:
            _clear_caches()
            st.rerun()
