import React, { FormEvent } from "react";
import { useDispatch, useSelector } from "react-redux";
import Modal from "react-bootstrap/Modal";
import Button from "react-bootstrap/Button";
import Form from "react-bootstrap/Form";
import { addPuzzle } from "./puzzlesSlice";
import { hideModal } from "./modalSlice";
import { selectHuntTags, selectHuntCreateChannelByDefault } from "./huntSlice";

import type { Dispatch } from "./store";
import type { HuntId, PuzzleTag } from "./types";

type InputChangeEvent = React.ChangeEvent<HTMLInputElement>;
type SelectChangeEvent = React.ChangeEvent<HTMLSelectElement>;

function guessNameFromUrl(urlish: string): string {
  let s = urlish.trim();
  if (!s) return "";
  s = s.split("#")[0].split("?")[0];
  s = s.replace(/\/+$/, "");

  const parts = s.split("/").filter(Boolean);
  if (parts.length === 0) return "";

  let slug = parts[parts.length - 1];

  try {
    slug = decodeURIComponent(slug);
  } catch {
    // ignore
  }

  // title case
  return slug
    .replace(/[-_]+/g, " ")
    .trim()
    .replace(/\b\w/g, (c) => c.toUpperCase());
}

function AddPuzzleModal({ huntId }: { huntId: HuntId }) {
  const allTags = useSelector(selectHuntTags);

  const [name, setName] = React.useState("");
  const [url, setUrl] = React.useState("");
  const [nameTouched, setNameTouched] = React.useState(false);

  const [assignedMeta, setAssignedMeta] = React.useState("");
  const [isMeta, setIsMeta] = React.useState(false);
  const [createChannels, setCreateChannels] = React.useState(
    useSelector(selectHuntCreateChannelByDefault)
  );

  const dispatch = useDispatch<Dispatch>();

  // guess name
  React.useEffect(() => {
    if (nameTouched) return;
    const guess = guessNameFromUrl(url);
    if (guess) setName(guess);
  }, [url, nameTouched]);

  const onSubmit = (e: FormEvent) => {
    e.preventDefault();
    dispatch(
      addPuzzle({
        huntId,
        name,
        url,
        is_meta: isMeta,
        create_channels: createChannels,
        assigned_meta: assignedMeta,
      })
    ).finally(() => {
      dispatch(hideModal());
    });
    return false;
  };

  return (
    <>
      <Modal.Header closeButton>
        <Modal.Title>Add Puzzle</Modal.Title>
      </Modal.Header>
      <Form onSubmit={onSubmit} autoComplete="off">
        <Modal.Body>
          <Form.Group controlId="addPuzzle.url">
            <Form.Label>Puzzle url</Form.Label>
            <Form.Control
              required
              placeholder="www.example.com/puzzles/my-puzzle"
              value={url}
              autoFocus
              onChange={(e: InputChangeEvent) => setUrl(e.target.value)}
            />
          </Form.Group>

          <Form.Group controlId="addPuzzle.name">
            <Form.Label>Puzzle name</Form.Label>
            <Form.Control
              required
              placeholder="Name"
              value={name}
              onChange={(e: InputChangeEvent) => {
                const v = e.target.value;
                setName(v);
                setNameTouched(v.trim().length > 0);
              }}
            />
          </Form.Group>

          <Form.Group controlId="addPuzzle.meta">
            <Form.Label>Assigned Round</Form.Label>
            <Form.Control
              as="select"
              value={assignedMeta}
              onChange={(e: SelectChangeEvent) => setAssignedMeta(e.target.value)}
            >
              <option key="none" value="">
                None
              </option>
              {allTags
                .filter((tag: PuzzleTag) => tag.is_meta)
                .map((tag: PuzzleTag) => (
                  <option key={tag.name} value={tag.name}>
                    {tag.name}
                  </option>
                ))}
            </Form.Control>
          </Form.Group>

          <Form.Check
            type="checkbox"
            label="Is round"
            id="is-meta-checkbox"
            checked={isMeta}
            onChange={(e: InputChangeEvent) => setIsMeta(e.target.checked)}
          />
          <Form.Check
            type="checkbox"
            label="Create discord channels"
            id="create-channels-checkbox"
            checked={createChannels}
            onChange={(e: InputChangeEvent) =>
              setCreateChannels(e.target.checked)
            }
          />
        </Modal.Body>
        <Modal.Footer>
          <Button variant="secondary" onClick={() => dispatch(hideModal())}>
            Cancel
          </Button>
          <Button variant="primary" type="submit">
            Add
          </Button>
        </Modal.Footer>
      </Form>
    </>
  );
}

export default AddPuzzleModal;
