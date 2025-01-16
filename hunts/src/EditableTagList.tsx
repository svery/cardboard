import React from "react";
import { useDispatch, useSelector } from "react-redux";
import {
  addPuzzleTag,
  deletePuzzleTag,
  selectPuzzleById,
} from "./puzzlesSlice";
import { SELECTABLE_TAG_COLORS } from "./constants";
import TagPill from "./TagPill";

import type { Dispatch, RootState } from "./store";
import type { PuzzleId, PuzzleTag } from "./types";

function EditableTagList({
  puzzleId,
  tags,
}: {
  puzzleId: PuzzleId;
  tags: PuzzleTag[];
}) {
  const selectPuzzleTags = React.useMemo(
    () => (state: RootState) => selectPuzzleById(state, puzzleId).tags,
    [puzzleId]
  );
  const puzzleTags = useSelector(selectPuzzleTags);
  const puzzleTagIds = new Set(puzzleTags.map((tag) => tag.id));
  const dispatch = useDispatch<Dispatch>();

  const selectable_colors = SELECTABLE_TAG_COLORS.map((tag) => tag.color);

  /* Breaks up tags into two rows: ones with hardcoded colors and then the selectable colors.
    In each row the tags are sorted by color and then by name. */
  const groupedTags = tags.sort((a, b) => a.color.localeCompare(b.color) || a.name.localeCompare(b.name)).reduce((result: PuzzleTag[][], item) => {
    if (selectable_colors.includes(item.color)) {
      if (result.length == 0) {
        result.push([]);
      }
      if (result.length == 1) {
        result.push([item]);
      } else {
        result[1].push(item);
      }
    } else if (result.length == 0) {
      result.push([item]);
    } else {
      result[0].push(item);
    }

    return result;
  }, []);

  return groupedTags.map((group) => (
    <div
      style={{
        display: "flex",
        alignItems: "center",
        flexWrap: "wrap",
      }}
    >
      {group.map((tag) => (
        <TagPill
          {...tag}
          selected={puzzleTagIds.has(tag.id)}
          faded={!puzzleTagIds.has(tag.id)}
          key={tag.name}
          onClick={() => {
            if (puzzleTagIds.has(tag.id)) {
              dispatch(deletePuzzleTag({ puzzleId, tagId: tag.id }));
            } else {
              dispatch(
                addPuzzleTag({
                  ...tag,
                  puzzleId,
                })
              );
            }
          }}
        />
      ))}
    </div>
  ));
}

export default EditableTagList;
